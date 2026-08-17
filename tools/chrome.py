#!/usr/bin/env python3
"""
Shared page chrome: <head>, header/nav, footer, and the section partials that
appear on more than one page (CTA band, quote form, FAQ, service grid, location
grid, breadcrumbs, icons).

This module is the ONLY place header and footer markup exists. topreno's real
maintenance hazard was chrome copy-pasted into every .html *and* duplicated
again inside its page generator — change a nav link there and you have to find
every copy. Here every page is generated, so there is exactly one copy.

Pages are written with root-absolute paths ("/services/decks/") and then piped
through relativize.py on the way out, which rewrites them to depth-correct
relative paths so the same files work locally, at the GitHub Pages project URL,
and at the custom domain.
"""

import html as _html
import json
import re as _re

import brand as S
import logo_dims


def plain(text):
    """HTML entities -> plain characters, for JSON-LD and meta attributes."""
    return _html.unescape(text)


def attr(text):
    """Escape a string for use inside a double-quoted HTML attribute."""
    return _html.escape(plain(text), quote=True)


# --- Icons ------------------------------------------------------------------
# Inline SVG only: no icon font, no extra requests, and they inherit currentColor.

_ICON_PATHS = {
    "tick": '<path d="M2.5 8.5l4 4 7-9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "arrow": '<path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "arrow-left": '<path d="M14 8H3M7 4L3 8l4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "phone": '<path d="M5.2 2.4 6.6 5 5.3 6.4a8 8 0 0 0 4.3 4.3L11 9.4l2.6 1.4v2.4c0 .6-.5 1.1-1.1 1a12 12 0 0 1-10.7-10.7c-.1-.6.4-1.1 1-1.1z" fill="currentColor"/>',
    "shield": '<path d="M8 1.5 13.5 4v4c0 3.2-2.3 5.7-5.5 6.5C4.8 13.7 2.5 11.2 2.5 8V4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M5.8 8.1 7.3 9.6l3-3.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "pin": '<path d="M8 1.5c2.5 0 4.5 2 4.5 4.5 0 3.3-4.5 8.5-4.5 8.5S3.5 9.3 3.5 6c0-2.5 2-4.5 4.5-4.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8" cy="6" r="1.8" fill="currentColor"/>',
    "quote": '<path d="M3.5 1.5h6L12.5 5v9.5h-9z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9.3 1.7V5h3.1M5.8 8.5h4.4M5.8 11h4.4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "mail": '<rect x="1.8" y="3.3" width="12.4" height="9.4" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m2.4 4.4 5.6 4 5.6-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "clock": '<circle cx="8" cy="8" r="6.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 4.4V8l2.6 1.6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "chevron": '<path d="M4 6l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
}


def icon(name, cls="ico", size=16):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 16 16" '
            f'aria-hidden="true" focusable="false">{_ICON_PATHS[name]}</svg>')


# --- Logo -------------------------------------------------------------------
# ONE logo: the designer's package in assets/img/brand/elitelogo/, published by
# tools/brand-assets.py. Every pixel on the site is the designer's — the only
# operations are resize and, for the header, crop. No redrawing, no recolouring,
# no re-typesetting. Favicons are the supplied favicon_io set, copied verbatim.
#
# Two lockups, both cut from that one file:
#
#   footer  the artwork WHOLE, exactly as supplied, clear space intact.
#   header  HORIZONTAL — mark and wordmark cropped apart and set side by side.
#           Approved by the owner 2026-08-16. The square stacked lockup squeezed
#           into a nav bar left "CARPENTRY & RENOVATIONS" about 5px tall, which
#           read as a smudge; side by side the wordmark gets the width it needs
#           and the sub-line clears ~8.5px.
#
# Neither lockup gets altered further without asking him first.
#
# No text is set alongside either one — the artwork already contains the company
# name, so adding words would print it twice. The accessible name comes from the
# link's aria-label and the img alt is empty, so a screen reader does not hear
# the brand twice either.

def _brand_img(name, asset, size, lazy):
    w, h = getattr(logo_dims, f"{name.upper()}_{asset}")
    loading = ' loading="lazy"' if lazy else ""
    return (f'<picture>'
            f'<source srcset="/assets/img/brand/{name}-{asset}.webp" type="image/webp">'
            f'<img class="{name}" src="/assets/img/brand/{name}-{asset}.png" alt=""'
            f' width="{round(size * w / h)}" height="{size}"'
            f' decoding="async"{loading}>'
            f'</picture>')


def logo(href="/", cls="logo", size=88, asset=480, lazy=False):
    """The stacked lockup, whole and unmodified — resized only. Footer use."""
    w, h = getattr(logo_dims, f"LOGO_{asset}")
    loading = ' loading="lazy"' if lazy else ""
    return (f'<a class="{cls}" href="{href}" aria-label="{attr(S.NAME_TEXT)} — home">'
            f'<picture>'
            f'<source srcset="/assets/img/brand/logo-{asset}.webp" type="image/webp">'
            f'<img src="/assets/img/brand/logo-{asset}.png" alt=""'
            f' width="{round(size * w / h)}" height="{size}"'
            f' decoding="async"{loading}>'
            f'</picture></a>')


def logo_row(href="/", cls="logo"):
    """The horizontal lockup for the header: mark then wordmark, side by side.

    Both pieces carry intrinsic width/height so the header reserves its space
    before the images decode — a logo that pops in and shoves the nav sideways
    is a layout shift on every first page view.
    """
    return (f'<a class="{cls}" href="{href}" aria-label="{attr(S.NAME_TEXT)} — home">'
            f'{_brand_img("mark", 192, 64, False)}'
            f'{_brand_img("word", 144, 46, False)}'
            f'</a>')


# --- Head -------------------------------------------------------------------

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Barlow+Condensed:wght@500;600;700&amp;family=Inter:wght@400;500;600;700&amp;display=swap">')


def head(title, desc, path, jsonld=None, noindex=False):
    url = f"{S.BASE}/{path}"
    robots = ("noindex, follow" if noindex
              else "index, follow, max-image-preview:large, max-snippet:-1")
    og = "" if noindex else f'''
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{attr(S.NAME_TEXT)}">
<meta property="og:locale" content="en_CA">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{S.BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{attr(S.NAME_TEXT)} logo — a chrome gable and EC monogram — beside the six services, for Cornwall and Akwesasne, Ontario.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(title)}">
<meta name="twitter:description" content="{attr(desc)}">
<meta name="twitter:image" content="{S.BASE}/assets/img/og-image.png">'''

    ld = ""
    if jsonld:
        ld = ('\n<script type="application/ld+json">\n'
              + json.dumps(jsonld, indent=2, ensure_ascii=False)
              + "\n</script>")

    return f'''<!DOCTYPE html>
<html lang="{S.LOCALE}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{attr(desc)}">
<meta name="robots" content="{robots}">{og}
<meta name="theme-color" content="#0B0B0C">
<link rel="icon" href="/assets/img/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon-16x16.png" sizes="16x16" type="image/png">
<link rel="icon" href="/assets/img/favicon-32x32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/main.js" defer></script>
<!-- .reveal starts at opacity:0 and is un-hidden by IntersectionObserver. If
     JS never runs, the copy must still be readable — this is a lead-gen site,
     not a demo. -->
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>{ld}
</head>
<body>'''


# --- Header -----------------------------------------------------------------

def _nav_link(label, href, current):
    aria = ' aria-current="page"' if current == href else ""
    return f'<li><a href="{href}"{aria}>{label}</a></li>'


def _nav_group(label, hub, items, current):
    """A top-level nav item with a sub-list. The sub-list is what carries the
    internal links to all six service / location pages from every page on the
    site, which is most of the internal-linking value."""
    cls = "has-sub in-section" if current.startswith(hub) else "has-sub"
    cur = ' aria-current="page"' if current == hub else ""
    subs = "".join(f'<li><a href="{href}">{text}</a></li>' for href, text in items)
    return (f'<li class="{cls}">'
            f'<a href="{hub}"{cur}>{label}{icon("chevron", "nav-caret", 14)}</a>'
            f'<ul class="nav-sub">{subs}</ul></li>')


def header(current=""):
    """`current` is the root-absolute path of the page, e.g. '/services/'."""
    svc_items = [(f"/services/{slug}/", label) for slug, label, _s, _b in S.SERVICES]
    loc_items = [(f"/locations/{slug}/", name) for slug, name, _s in S.LOCATIONS]

    return f'''<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap">
    {logo_row()}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="nav-list">
        {_nav_link("Home", "/", current)}
        {_nav_group("Services", "/services/", svc_items, current)}
        {_nav_group("Service areas", "/locations/", loc_items, current)}
        {_nav_link("About", "/about/", current)}
        {_nav_link("Contact", "/contact/", current)}
      </ul>
      <div class="nav-actions">
        <a class="nav-phone" href="{S.PHONE_HREF}">{icon("phone", "ico", 15)}<span>{S.PHONE_DISPLAY}</span></a>
        <a class="btn btn-primary btn-sm" href="/contact/">Get a free quote</a>
      </div>
    </nav>
  </div>
</header>
<div class="stripe stripe-thin" aria-hidden="true"></div>'''


# --- Footer -----------------------------------------------------------------

def footer(minimal=False):
    if minimal:
        return f'''<footer class="site-footer">
  <div class="stripe" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> {S.NAME}. All rights reserved.</span>
    </div>
  </div>
</footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();</script>
</body>
</html>'''

    svc = "".join(f'<li><a href="/services/{s}/">{short}</a></li>'
                  for s, _label, short, _b in S.SERVICES)
    loc = "".join(f'<li><a href="/locations/{s}/">{name}</a></li>'
                  for s, name, _short in S.LOCATIONS)

    return f'''<footer class="site-footer">
  <div class="stripe" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
{logo("/", "footer-mark", size=200, asset=480, lazy=True)}
        <p>{S.TAGLINE}</p>
        <p class="footer-badge">{icon("shield")} Licensed &amp; fully insured &middot; WSIB covered</p>
      </div>
      <div class="footer-col">
        <h3>Services</h3>
        <ul>{svc}</ul>
      </div>
      <div class="footer-col">
        <h3>Service areas</h3>
        <ul>{loc}</ul>
      </div>
      <div class="footer-col">
        <h3>Get in touch</h3>
        <ul>
          <li><a href="{S.PHONE_HREF}">{icon("phone")} {S.PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{S.EMAIL}">{icon("mail")} {S.EMAIL}</a></li>
          <li class="plain">{icon("clock")} {S.HOURS["display"]}</li>
          <li><a href="/contact/">Request a quote</a></li>
          <li><a href="/about/">About us</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> {S.NAME}. All rights reserved.</span>
      <span class="footer-meta">Serving {S.CITY}, Akwesasne &amp; Stormont, Dundas and Glengarry.</span>
    </div>
  </div>
</footer>
<a class="call-bar" href="{S.PHONE_HREF}">{icon("phone", "ico", 18)} Call {S.SHORT} &middot; {S.PHONE_DISPLAY}</a>
<script>document.getElementById('year').textContent=new Date().getFullYear();</script>
</body>
</html>'''


# --- Section partials -------------------------------------------------------

def breadcrumbs(trail):
    """`trail` is a list of (label, href) with href=None for the current page."""
    items = []
    for label, href in trail:
        if href:
            items.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            items.append(f'<li><span aria-current="page">{label}</span></li>')
    return ('<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>'
            + "".join(items) + "</ol></nav>")


def breadcrumb_ld(trail):
    """Matching BreadcrumbList for `trail`; the current page needs a URL too."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": plain(label),
             "item": f"{S.BASE}{href}"}
            for i, (label, href) in enumerate(trail)
        ],
    }


def page_hero(eyebrow, h1, lead, trail, quote_href="#quote"):
    """`quote_href` must point at a form that actually exists on the page — use
    '/contact/' on pages that do not embed one, or the CTA is a dead anchor."""
    return f'''<section class="page-hero grid-bg">
  <div class="wrap">
    {breadcrumbs(trail)}
    <p class="eyebrow reveal">{eyebrow}</p>
    <h1 class="reveal">{h1}</h1>
    <p class="lead reveal reveal-1">{lead}</p>
    <div class="hero-cta reveal reveal-2">
      <a class="btn btn-primary" href="{quote_href}">Get a free quote{icon("arrow")}</a>
      <a class="btn btn-ghost" href="{S.PHONE_HREF}">{icon("phone")} {S.PHONE_DISPLAY}</a>
    </div>
  </div>
</section>'''


def trust_bar():
    cells = "".join(
        f'<li>{icon(ic, "ico trust-ico", 20)}<span><strong>{title}</strong>{sub}</span></li>'
        for ic, title, sub in S.TRUST_POINTS
    )
    return f'<section class="trust-bar"><div class="wrap"><ul>{cells}</ul></div></section>'


def cta_band(heading, sub, button="Request your free quote"):
    return f'''<section class="cta-band">
  <div class="wrap">
    <div class="cta-inner">
      <div>
        <h2>{heading}</h2>
        <p>{sub}</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-primary" href="/contact/">{button}{icon("arrow")}</a>
        <a class="btn btn-ghost" href="{S.PHONE_HREF}">{icon("phone")} {S.PHONE_DISPLAY}</a>
      </div>
    </div>
  </div>
</section>'''


def service_grid(exclude=None, heading="What we build", intro=None, dark=True):
    cards = []
    for i, (slug, _label, short, blurb) in enumerate(S.SERVICES, 1):
        if slug == exclude:
            continue
        cards.append(f'''<a class="card card-dark card-link reveal" href="/services/{slug}/">
  <span class="card-num">{i:02d}</span>
  <h3>{short}</h3>
  <p>{blurb}</p>
  <span class="arrow-link">Read more{icon("arrow")}</span>
</a>''')
    lead = f'<p class="lead">{intro}</p>' if intro else ""
    cls = "section steel" if dark else "section"
    return f'''<section class="{cls}" id="services">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Services</p>
      <h2>{heading}</h2>
      {lead}
    </div>
    <div class="card-grid cols-3">{"".join(cards)}</div>
  </div>
</section>'''


def location_grid(exclude=None, heading="Where we work"):
    cards = []
    for slug, name, _short in S.LOCATIONS:
        if slug == exclude:
            continue
        cards.append(f'<a class="loc reveal" href="/locations/{slug}/">'
                     f'<span>{name}</span>{icon("arrow")}</a>')
    return f'''<section class="section section-sm">
  <div class="wrap">
    <div class="section-head head-split">
      <div>
        <p class="eyebrow">Service areas</p>
        <h2>{heading}</h2>
      </div>
      <p class="lead">Based in {S.CITY} and working across Stormont, Dundas and Glengarry.
      If your town is not listed, call us anyway &mdash; we travel.</p>
    </div>
    <div class="loc-grid">{"".join(cards)}</div>
  </div>
</section>'''


def faq_section(items, heading="Frequently asked questions", eyebrow="FAQ"):
    """items: list of (question, answer_html). Returns (html, FAQPage node).

    Every schema entry mirrors a visible <details> block verbatim. Invisible FAQ
    markup is a manual-action risk, so the two are generated from one list.
    """
    blocks = "".join(
        f'<details class="faq-item"><summary>{q}</summary><div class="faq-body">{a}</div></details>'
        for q, a in items
    )
    ld = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(_strip_tags(a))}}
            for q, a in items
        ],
    }
    html_out = f'''<section class="section faq">
  <div class="wrap wrap-narrow">
    <div class="section-head">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{heading}</h2>
    </div>
    {blocks}
  </div>
</section>'''
    return html_out, ld


_TAG = _re.compile(r"<[^>]+>")


def _strip_tags(s):
    return _re.sub(r"\s+", " ", _TAG.sub("", s)).strip()


# --- Quote form -------------------------------------------------------------

def quote_form(source, compact=False, heading="Request a free quote",
               sub=None, preselect=None):
    """`source` is written into a hidden field so the owner can see which page
    produced the lead — one Formspree endpoint, still attributable."""
    opts = "".join(
        f'<option value="{attr(short)}"{" selected" if slug == preselect else ""}>{short}</option>'
        for slug, _l, short, _b in S.SERVICES
    )
    sub = sub or ("Tell us what you are planning. We reply to every inquiry, usually "
                  "within one business day.")
    extra = "" if compact else '''
      <div class="field">
        <label for="f-address">Project address <span class="opt">(optional)</span></label>
        <input type="text" id="f-address" name="address" autocomplete="street-address">
      </div>
      <div class="field">
        <label for="f-timing">When are you hoping to start?</label>
        <select id="f-timing" name="timing">
          <option value="">Select&hellip;</option>
          <option>As soon as possible</option>
          <option>Within 1&ndash;3 months</option>
          <option>Within 3&ndash;6 months</option>
          <option>Just planning / budgeting</option>
        </select>
      </div>'''

    return f'''<section class="section quote-section" id="quote">
  <div class="wrap wrap-narrow">
    <div class="section-head">
      <p class="eyebrow">Free quote</p>
      <h2>{heading}</h2>
      <p class="lead">{sub}</p>
    </div>
    <form class="quote-form" id="quoteForm" action="{S.FORM_ACTION}" method="POST" novalidate>
      <div class="field-row">
        <div class="field">
          <label for="f-name">Name <span class="req" aria-hidden="true">*</span></label>
          <input type="text" id="f-name" name="name" required autocomplete="name">
        </div>
        <div class="field">
          <label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label>
          <input type="tel" id="f-phone" name="phone" required autocomplete="tel">
        </div>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
          <input type="email" id="f-email" name="email" required autocomplete="email">
        </div>
        <div class="field">
          <label for="f-service">What do you need?</label>
          <select id="f-service" name="service">
            <option value="">Select a service&hellip;</option>
            {opts}
            <option>Something else</option>
          </select>
        </div>
      </div>{extra}
      <div class="field">
        <label for="f-message">Project details <span class="req" aria-hidden="true">*</span></label>
        <textarea id="f-message" name="message" rows="5" required
          placeholder="Rough size, materials you have in mind, and anything else that helps us quote accurately."></textarea>
      </div>

      <div class="hp" aria-hidden="true">
        <label for="_gotcha">Leave this field empty</label>
        <input type="text" id="_gotcha" name="_gotcha" tabindex="-1" autocomplete="off">
      </div>
      <input type="hidden" name="_subject" value="{attr(S.FORM_SUBJECT)}">
      <input type="hidden" name="page" value="{attr(source)}">

      <div class="form-footer">
        <button type="submit" class="btn btn-primary btn-submit">Send my request{icon("arrow")}</button>
        <p class="form-note">No obligation, no sales calls. We use your details only to reply
        to this request.</p>
        <div class="form-msg ok" id="formOk" role="status" tabindex="-1">
          {icon("tick")} Thanks &mdash; your request is in. We will be in touch shortly.
        </div>
        <div class="form-msg err" id="formErr" role="alert">
          Something went wrong sending that. Please call
          <a href="{S.PHONE_HREF}">{S.PHONE_DISPLAY}</a> or email
          <a href="mailto:{S.EMAIL}">{S.EMAIL}</a> instead.
        </div>
      </div>
    </form>
  </div>
</section>'''


# --- Business JSON-LD -------------------------------------------------------

BUSINESS_ID = f"{S.BASE}/#business"
PERSON_ID = f"{S.BASE}/#owner"


def person_node():
    """The full Person node for the owner. Only emitted on /about/.

    Three properties carry the ownership between them, because no single one
    can: `jobTitle: Owner` on this node, `founder` pointing here from the
    business, and `worksFor` pointing back. `worksFor` is affiliation, not
    employment status — it says which company he is part of, and the bio says
    plainly that he is on the tools. Read together the graph is unambiguous:
    Jake Martin owns this company and works in it.

    Every other page carries a name-only stub inside the business node's
    `founder`, so no page ever ships a bare @id reference to something it does
    not describe. The rich version lives where the biography and the photograph
    actually are, which is also where it earns its keep.

    `description` deliberately paraphrases the visible copy on that page rather
    than saying anything new — structured data that asserts more than the reader
    can see is the exact pattern manual actions are written for.
    """
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": S.OWNER_NAME,
        "jobTitle": S.OWNER_ROLE,
        "worksFor": {"@id": BUSINESS_ID},
        "image": f"{S.BASE}/assets/img/team/jake-480.jpg",
        "mainEntityOfPage": f"{S.BASE}/about/",
        "description": ("Close to a decade in the trade, across windows, siding, "
                        "fencing, decks, bathrooms and complete kitchen renovations."),
        "knowsAbout": [
            "Deck building", "Fence installation", "Vinyl siding",
            "Window replacement", "Bathroom renovation", "Kitchen renovation",
            "Finish carpentry",
        ],
    }


def business_node(full=True):
    node = {
        "@type": "GeneralContractor",
        "@id": BUSINESS_ID,
        "name": S.NAME_TEXT,
        "url": f"{S.BASE}/",
        "telephone": S.PHONE_E164,
        "email": S.EMAIL,
        "image": f"{S.BASE}/assets/img/og-image.png",
        "logo": f"{S.BASE}/assets/img/android-chrome-512x512.png",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": S.CITY,
            "addressRegion": S.REGION,
            "addressCountry": S.COUNTRY,
        },
        "areaServed": [{"@type": "City", "name": n} for n in S.AREA_SERVED],
        # He OWNS this company. schema.org has no Organization -> Person "owner"
        # property, so `founder` is the correct available idiom for an
        # owner-operator; `employee` would say he works here for somebody else.
        #
        # Name-only stub so this is a complete statement on every page. /about/
        # additionally carries the full Person node under the same @id, and the
        # two merge in any consumer that reads both.
        "founder": {"@type": "Person", "@id": PERSON_ID, "name": S.OWNER_NAME},
    }
    if S.SAME_AS:
        node["sameAs"] = S.SAME_AS
    if full:
        node["description"] = plain(S.TAGLINE)
        node["knowsAbout"] = [
            "Deck building", "Fence installation", "Vinyl siding",
            "Window replacement", "Bathroom renovation", "Kitchen renovation",
            "Finish carpentry", "Ontario Building Code",
        ]
        node["openingHoursSpecification"] = [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": S.HOURS["days"],
            "opens": S.HOURS["opens"],
            "closes": S.HOURS["closes"],
        }]
        node["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": "Carpentry and renovation services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {
                    "@type": "Service", "name": plain(short),
                    "description": plain(blurb),
                    "url": f"{S.BASE}/services/{slug}/"}}
                for slug, _l, short, blurb in S.SERVICES
            ],
        }
    return node
