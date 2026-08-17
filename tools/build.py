#!/usr/bin/env python3
"""
Build every page in the site.

    python3 tools/build.py

Writes 18 HTML pages plus sitemap.xml, robots.txt and site.webmanifest, then
runs relativize.py so all root-absolute href/src values become depth-correct
relative paths. That is what lets the identical files work locally, at the
GitHub Pages project URL, and at the custom domain.

Every page is generated, so header and footer markup exists in exactly one
place (chrome.py). Edit copy in content_services.py / content_locations.py or
in the body builders below, then re-run this script.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import brand as S              # noqa: E402
import chrome as C             # noqa: E402
from content_services import SERVICES as SVC, PHOTOS   # noqa: E402
from content_locations import LOCATIONS as LOC # noqa: E402
from content_projects import PROJECTS          # noqa: E402
from relativize import relativize              # noqa: E402

PAGES = []   # (path, priority, changefreq) for sitemap.xml


def write(path, html, priority="0.8", changefreq="monthly", in_sitemap=True):
    """`path` is the URL path: '' for the root, 'services/decks/' for a page."""
    out_dir = os.path.join(ROOT, path)
    os.makedirs(out_dir, exist_ok=True)
    depth = path.count("/") if path else 0
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(relativize(html, depth))
    if in_sitemap:
        PAGES.append((path, priority, changefreq))
    print(f"  /{path}")


SEO_WARNINGS = []


def doc(title, desc, path, body, graph, current, noindex=False, minimal_footer=False):
    # Google truncates titles past roughly 60 characters and descriptions past
    # roughly 160. Warn at build time so a rewrite cannot silently regress into
    # ellipsised search results.
    if not noindex:
        t, d = len(C.plain(title)), len(C.plain(desc))
        if t > 60:
            SEO_WARNINGS.append(f"/{path} title is {t} chars (max 60)")
        if d > 158 or d < 70:
            SEO_WARNINGS.append(f"/{path} description is {d} chars (target 70-158)")

    ld = {"@context": "https://schema.org", "@graph": graph} if graph else None
    return (C.head(title, desc, path, ld, noindex)
            + C.header(current)
            + f'<main id="main">{body}</main>'
            + C.footer(minimal=minimal_footer))


def tick_list(items):
    return "".join(f'<li>{C.icon("tick")}<span>{i}</span></li>' for i in items)


# Which services have a real job photo, from the `service` key in PROJECTS.
# A page uses the owner's own work whenever one exists and falls back to stock
# otherwise, so adding a photo to content_projects.py is all it takes to retire
# a stock image.
REAL_FIGURES = {p["service"]: p for p in PROJECTS if p.get("service")}


def figure(base, alt, caption=None, real=False):
    """A 16:10 <picture> with WebP first.

    Both sources are pre-cropped to 16:10 — stock by fetch-photos.py, real work
    by project-photos.py — so width/height match what is painted and there is
    no layout shift.

    `real` picks the folder AND decides whether a caption is allowed at all.
    Only the owner's own work gets one; stock is never captioned, because a
    caption under a photo reads as a claim about the photo.
    """
    folder = "projects" if real else "photos"
    cap = f"\n  <figcaption>{caption}</figcaption>" if caption else ""
    return f'''<figure class="figure reveal">
  <picture>
    <source srcset="/assets/img/{folder}/{base}.webp" type="image/webp">
    <img src="/assets/img/{folder}/{base}.jpg" alt="{C.attr(alt)}"
         width="1400" height="875" loading="lazy" decoding="async">
  </picture>{cap}
</figure>'''


def service_figure(slug):
    """The owner's own work if there is any for this service, else stock."""
    p = REAL_FIGURES.get(slug)
    if p:
        return figure(f'{p["slug"]}-wide', p["alt"], caption=p["caption"], real=True)
    base, alt = PHOTOS[slug]
    return figure(base, alt)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

HOME_FAQS = [
    ("What areas do you serve?",
     "<p>Cornwall and Akwesasne are our two core areas, and we work across Stormont, "
     "Dundas and Glengarry &mdash; Long Sault, Ingleside, Glen Walter, Lancaster, "
     "Williamstown, Martintown, Summerstown, Maxville and Alexandria among them. There is no "
     "travel surcharge within that area. If your town is not listed, call and ask.</p>"),
    ("Are you licensed and insured?",
     "<p>Yes. We carry liability insurance and WSIB coverage, and we are happy to provide "
     "certificates before work starts &mdash; you should ask any contractor for both, and be "
     "wary of one who hesitates. Uninsured work on your property can leave you exposed if "
     "someone is hurt.</p>"),
    ("Do you charge for quotes?",
     "<p>No. Quotes are free, provided in writing and itemised so you can see what is "
     "driving the cost and adjust the scope if you want to. We do not use high-pressure "
     "sales tactics and we do not do same-day-discount pricing.</p>"),
    ("Do you handle building permits?",
     "<p>Yes. Where a permit is required we prepare the drawings and file the application "
     "with the right authority &mdash; which is not always the City of Cornwall. Long Sault "
     "and Ingleside go through South Stormont, Lancaster and Glen Walter through South "
     "Glengarry, Alexandria through North Glengarry, and the Ontario portion of Akwesasne "
     "through the Mohawk Council of Akwesasne. We deal with whichever applies.</p>"),
    ("How far ahead should I book?",
     "<p>For exterior work &mdash; decks, fencing, siding &mdash; as early as you can. The "
     "building season here is short and spring books up quickly. Interior work like bathrooms "
     "and kitchens is much easier to schedule through the autumn and winter, and winter is a "
     "genuinely good time to do it.</p>"),
    ("What happens after I send a quote request?",
     "<p>We call you back, usually within one business day, to talk through what you are "
     "planning. If it looks like a fit we book a site visit to measure and look at the "
     "conditions, then send a written, itemised quote. No obligation at any stage, and we "
     "will tell you if we think your money is better spent on something else.</p>"),
]

PROCESS = [
    ("Talk it through", "A phone call or an email to understand what you are planning, what "
                        "matters most to you, and whether we are the right crew for it."),
    ("Site visit and measure", "We come out, measure, look at the conditions, and check "
                               "setbacks, permits and anything hidden that will affect the price."),
    ("Written, itemised quote", "A quote you can actually read, broken down by line so you "
                                "can see the cost drivers and adjust the scope if you want."),
    ("Build and clean up", "One crew, a schedule you were given in advance, permits and "
                           "inspections handled, and the site left clean at the end of it."),
]

VALUES = [
    ("shield", "Licensed and fully insured",
     "Liability insurance and WSIB coverage on every job. Certificates available before we "
     "start &mdash; ask us, and ask everyone else you are considering."),
    ("quote", "Written quotes, itemised",
     "You get a document that shows what each part of the job costs, so you can compare "
     "properly and change the scope without renegotiating from scratch."),
    ("tick", "One crew, start to finish",
     "The people who quote your job are the people who build it. No subcontracted mystery "
     "crew turning up on day one who have never seen the quote."),
    ("pin", "We know these houses",
     "Cornwall's post-war stock, the 1957&ndash;58 Seaway villages, Glengarry's rural "
     "properties &mdash; we have opened enough of these walls to price the surprises "
     "realistically instead of discovering them mid-job."),
    ("clock", "Schedules we actually keep",
     "You get a written schedule and we tell you early if anything moves. Silence is the "
     "thing homeowners hate most about renovation work, and it is avoidable."),
    ("mail", "Straight answers",
     "If a repair is smarter than a replacement, we will say so. If your budget is not "
     "realistic for the scope, we will say that too, before you have spent anything."),
]


def build_home():
    hero_points = [
        "Licensed &amp; fully insured", "Free written quotes",
        "Permits handled", "Cornwall &amp; Akwesasne",
    ]
    points = "".join(f'<li>{C.icon("tick")}{p}</li>' for p in hero_points)

    values = "".join(
        f'<div class="value reveal">{C.icon(ic, "ico", 20)}<div><h3>{t}</h3><p>{b}</p></div></div>'
        for ic, t, b in VALUES)

    steps = "".join(
        f'<div class="step reveal"><b>{i:02d}</b><h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(PROCESS, 1))

    faq_html, faq_ld = C.faq_section(HOME_FAQS, "Questions homeowners ask us")

    # Real project photos. These are the company's own work, so unlike the stock
    # imagery still running on three of the service pages they may be presented
    # as theirs.
    #
    # Built as a scroll-snap carousel: the viewport is natively scrollable and
    # swipeable, so every photo remains reachable with no JavaScript at all.
    # main.js only adds the buttons and dots on top. There is deliberately no
    # auto-advance — it steals control from the reader and is a well-known
    # accessibility problem.
    n = len(PROJECTS)
    slides = "".join(
        f'''<li class="slide" id="slide-{i}" role="group" aria-roledescription="slide"
    aria-label="Project {i} of {n}: {C.attr(p["tag"])}">
  <div class="slide-media">
    <picture>
      <source srcset="/assets/img/projects/{p["slug"]}.webp" type="image/webp">
      <img src="/assets/img/projects/{p["slug"]}.jpg" alt="{C.attr(p["alt"])}"
           width="800" height="1067" loading="lazy" decoding="async">
    </picture>
  </div>
  <div class="slide-body">
    <span class="shot-tag">{p["tag"]}</span>
    <p>{p["caption"]}</p>
    <a class="arrow-link" href="{p["href"]}">{p["link"]}{C.icon("arrow")}</a>
  </div>
</li>''' for i, p in enumerate(PROJECTS, 1))

    # `current` is built outside the f-string: an escaped quote inside an
    # f-string expression is a syntax error before Python 3.12.
    def dot(i):
        current = ' aria-current="true"' if i == 1 else ""
        return (f'<button type="button" class="car-dot" data-go="{i - 1}" '
                f'aria-label="Show project {i} of {n}"{current}>'
                f'<span></span></button>')

    dots = "".join(dot(i) for i in range(1, n + 1))

    carousel = f'''<div class="carousel" data-carousel>
  <div class="carousel-viewport" tabindex="0" role="group"
       aria-roledescription="carousel" aria-label="Recent projects">
    <ol class="carousel-track">{slides}</ol>
  </div>
  <div class="carousel-ui">
    <button type="button" class="car-btn" data-prev aria-label="Previous project">
      {C.icon("arrow-left", "ico", 18)}</button>
    <div class="car-dots">{dots}</div>
    <button type="button" class="car-btn" data-next aria-label="Next project">
      {C.icon("arrow", "ico", 18)}</button>
  </div>
</div>'''

    body = f'''
<section class="hero grid-bg">
  <div class="wrap">
    <p class="eyebrow reveal">Cornwall &amp; Akwesasne, Ontario</p>
    <h1 class="reveal">Built right,<br><span class="em">the first time.</span></h1>
    <p class="lead reveal reveal-1">{S.TAGLINE} Licensed, fully insured, and straight with you
    about what your project actually needs.</p>
    <div class="hero-cta reveal reveal-2">
      <a class="btn btn-primary" href="/contact/">Get a free quote{C.icon("arrow")}</a>
      <a class="btn btn-ghost" href="{S.PHONE_HREF}">{C.icon("phone")} {S.PHONE_DISPLAY}</a>
    </div>
    <ul class="hero-points reveal reveal-3">{points}</ul>
  </div>
</section>

{C.trust_bar()}

{C.service_grid(heading="Six trades, one crew",
                intro="Exterior and interior work across Cornwall, Akwesasne and SD&amp;G. "
                      "Every one of these is quoted in writing and itemised.",
                dark=True)}

<section class="section">
  <div class="wrap">
    <div class="section-head head-split">
      <div>
        <p class="eyebrow">Why us</p>
        <h2>The boring things that actually matter</h2>
      </div>
      <p class="lead">Anyone can build a deck that looks good in week one. What separates
      contractors is the work you cannot see and the way they behave when something
      unexpected turns up.</p>
    </div>
    <div class="value-grid">{values}</div>
  </div>
</section>

<section class="section process">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2>From first call to final cleanup</h2>
      <p class="lead">No surprises, and no stage where you are left wondering what happens next.</p>
    </div>
    <div class="step-grid">{steps}</div>
  </div>
</section>

<section class="section section-sm" id="projects">
  <div class="wrap">
    <div class="section-head head-split">
      <div>
        <p class="eyebrow">Our work</p>
        <h2>Recent projects</h2>
      </div>
      <p class="lead">Decks, porches and verandas, a bathroom, a kitchen and finish
      carpentry &mdash; all photographed on our own job sites. Siding and window
      projects are being added as jobs wrap up.</p>
    </div>
    {carousel}
    <p class="gallery-note">Want to see more, or an address you can drive past?
    <a href="/contact/">Ask us</a> &mdash; we are happy to provide references.</p>
  </div>
</section>

{C.location_grid()}

{faq_html}

{C.cta_band("Ready to get a number you can trust?",
            "Tell us what you are planning. We reply to every inquiry, usually within one "
            "business day, and the quote is free either way.")}
'''

    graph = [
        C.business_node(full=True),
        {"@type": "WebSite", "@id": f"{S.BASE}/#website", "url": f"{S.BASE}/",
         "name": S.NAME_TEXT, "publisher": {"@id": C.BUSINESS_ID}, "inLanguage": "en-CA"},
        faq_ld,
    ]
    write("", doc(
        "Carpentry &amp; Renovations Cornwall ON | Elite Carpentry",
        "Licensed, insured carpentry and renovation contractors in Cornwall and Akwesasne. "
        "Decks, fencing, siding, windows, bathrooms and kitchens.",
        "", body, graph, "/"), priority="1.0", changefreq="weekly")


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def build_services_hub():
    trail = [("Home", "/"), ("Services", "/services/")]
    body = f'''
{C.page_hero("Services", "Carpentry &amp; Renovation Services in Cornwall",
             "Six things we do properly, rather than everything done adequately. Exterior "
             "and interior work across Cornwall, Akwesasne and Stormont, Dundas and Glengarry.",
             trail, quote_href="/contact/")}

{C.trust_bar()}

{C.service_grid(heading="What we build", dark=False)}

<section class="section steel">
  <div class="wrap wrap-narrow">
    <div class="section-head">
      <p class="eyebrow">Scope</p>
      <h2>What we do not do</h2>
    </div>
    <div class="prose">
      <p class="lead">It is a fair question, and the answer tells you more than a list of
      services does.</p>
      <p>We are a carpentry and renovation crew. We do not do roofing, we are not an HVAC
      company, and we do not take on new-build houses. Plumbing and electrical work on our
      projects is carried out by licensed trades that we schedule and coordinate &mdash; we
      manage it, we do not pretend to hold the licences ourselves.</p>
      <p>If your project needs something outside what we do, we will tell you at the quote
      stage and point you at someone who does it well. That is a better outcome for everyone
      than us learning on your house.</p>
    </div>
  </div>
</section>

{C.location_grid()}

{C.cta_band("Not sure which of these you need?",
            "Describe the problem rather than the solution and we will tell you what the job "
            "actually is. Quotes are free and there is no obligation.")}
'''
    graph = [
        C.breadcrumb_ld(trail),
        {"@type": "Service",
         "name": "Carpentry and renovation services",
         "serviceType": "Carpentry and renovation",
         "provider": {"@id": C.BUSINESS_ID},
         "areaServed": [{"@type": "City", "name": n} for n in S.AREA_SERVED],
         "hasOfferCatalog": {
             "@type": "OfferCatalog", "name": "Services",
             "itemListElement": [
                 {"@type": "Offer", "itemOffered": {
                     "@type": "Service", "name": C.plain(short),
                     "url": f"{S.BASE}/services/{slug}/"}}
                 for slug, _l, short, _b in S.SERVICES]}},
    ]
    write("services/", doc(
        "Renovation Services in Cornwall ON | Elite Carpentry",
        "Decks, fencing, siding, windows, bathroom and kitchen renovations in Cornwall, "
        "Akwesasne and SD&G. Licensed, insured, free written quotes.",
        "services/", body, graph, "/services/"), priority="0.9")


def build_service(slug):
    d = SVC[slug]
    trail = [("Home", "/"), ("Services", "/services/"), (d["nav"], f"/services/{slug}/")]

    intro = "".join(f"<p>{p}</p>" for p in d["intro"])

    items = "".join(
        f'<div class="svc-item reveal"><h3>{C.icon("tick")}<span>{t}</span></h3><p>{b}</p></div>'
        for t, b in d["items"])

    options = "".join(
        f'''<div class="card reveal">
  <h3>{name}</h3>
  <p>{body}</p>
  <ul class="card-list">{tick_list(bullets)}</ul>
</div>''' for name, body, bullets in d["options"])

    c_head, c_body = d["callout"]
    faq_html, faq_ld = C.faq_section(d["faqs"], f"{d['nav']}: common questions")

    body = f'''
{C.page_hero(d["eyebrow"], d["h1"], d["lead"], trail)}

{C.trust_bar()}

<section class="section">
  <div class="wrap">
    <div class="media-split">
      <div class="media-split-text prose">{intro}</div>
      {service_figure(slug)}
    </div>
  </div>
</section>

<section class="section section-sm steel">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Scope of work</p>
      <h2>{d["items_head"]}</h2>
    </div>
    <div class="svc-items">{items}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Options</p>
      <h2>{d["options_head"]}</h2>
      <p class="lead">{d["options_intro"]}</p>
    </div>
    <div class="card-grid cols-3">{options}</div>
  </div>
</section>

<section class="section section-sm">
  <div class="wrap wrap-narrow">
    <div class="callout reveal">
      <h3>{c_head}</h3>
      {c_body}
    </div>
  </div>
</section>

{C.location_grid(heading=f"{d['nav']} across Cornwall &amp; SD&amp;G")}

{faq_html}

{C.quote_form(f"Service: {C.plain(d['nav'])}", compact=False,
              heading=f"Get a free quote for your {C.plain(d['nav']).lower().rstrip('s')} project"
              if slug not in ("bathroom-renovations", "kitchen-renovations")
              else f"Get a free quote for your {C.plain(d['nav']).lower()} project",
              preselect=slug)}

{C.service_grid(exclude=slug, heading="Other things we do", dark=True)}

{C.cta_band("Prefer to talk it through first?",
            "Call us and describe what you are dealing with. We will tell you honestly "
            "whether it is a job worth doing now.")}
'''
    graph = [
        C.breadcrumb_ld(trail),
        {"@type": "Service",
         "name": C.plain(d["h1"]),
         "serviceType": d["service_type"],
         "description": C.plain(d["desc"]),
         "url": f"{S.BASE}/services/{slug}/",
         "provider": {"@id": C.BUSINESS_ID},
         "areaServed": [{"@type": "City", "name": n} for n in S.AREA_SERVED]},
        faq_ld,
    ]
    write(f"services/{slug}/", doc(d["title"], C.plain(d["desc"]),
                                   f"services/{slug}/", body, graph,
                                   f"/services/{slug}/"), priority="0.8")


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

def build_locations_hub():
    trail = [("Home", "/"), ("Service areas", "/locations/")]
    cards = ""
    for slug, name, _short in S.LOCATIONS:
        d = LOC[slug]
        cards += f'''<a class="card card-link reveal" href="/locations/{slug}/">
  <span class="card-num">{d["region"]}</span>
  <h3>{name}</h3>
  <p>{d["lead"]}</p>
  <ul class="card-list">{tick_list(d["areas"][:3])}</ul>
  <span class="arrow-link">See {name}{C.icon("arrow")}</span>
</a>'''

    body = f'''
{C.page_hero("Service areas", "Where We Work",
             "Based in Cornwall, working across Akwesasne and Stormont, Dundas and Glengarry. "
             "No travel surcharge anywhere in this list.",
             trail, quote_href="/contact/")}

{C.trust_bar()}

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Six areas</p>
      <h2>Local means local</h2>
      <p class="lead">These are not pages we wrote to rank. They are the places we actually
      work, and each one has its own building department, its own housing stock and its own
      set of things that go wrong.</p>
    </div>
    <div class="card-grid cols-3">{cards}</div>
  </div>
</section>

<section class="section steel">
  <div class="wrap wrap-narrow">
    <div class="section-head">
      <p class="eyebrow">Not on the list?</p>
      <h2>Ask anyway</h2>
    </div>
    <div class="prose">
      <p class="lead">We regularly work in Williamstown, Martintown, Summerstown, Bainsville,
      Maxville, Moose Creek, Newington, Avonmore, St.&nbsp;Andrew&rsquo;s West and Green Valley,
      among others.</p>
      <p>Stormont, Dundas and Glengarry is a big area with a small population, so we cover a
      lot of ground. If you are within reasonable driving distance of Cornwall, the answer is
      probably yes &mdash; and if it is not, we will say so straight away rather than quoting a
      job we cannot service properly.</p>
    </div>
  </div>
</section>

{C.cta_band("Tell us where you are",
            "Send us your address and what you are planning. We will tell you whether we "
            "cover it and what the job is likely to involve.")}
'''
    graph = [
        C.breadcrumb_ld(trail),
        {"@type": "ItemList",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": C.plain(name),
              "item": f"{S.BASE}/locations/{slug}/"}
             for i, (slug, name, _s) in enumerate(S.LOCATIONS)]},
    ]
    write("locations/", doc(
        "Service Areas &mdash; Cornwall &amp; SD&amp;G | Elite Carpentry",
        "Carpentry and renovation services across Cornwall, Akwesasne, Long Sault, Ingleside, "
        "Lancaster, Glen Walter and Alexandria. No travel surcharge.",
        "locations/", body, graph, "/locations/"), priority="0.9")


def build_location(slug):
    d = LOC[slug]
    name = d["name"]
    trail = [("Home", "/"), ("Service areas", "/locations/"), (name, f"/locations/{slug}/")]

    intro = "".join(f"<p>{p}</p>" for p in d["intro"])
    notes = "".join(
        f'<div class="card card-dark reveal"><span class="card-num">{i:02d}</span>'
        f'<h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(d["notes"], 1))

    faq_html, faq_ld = C.faq_section(d["faqs"], f"{name}: common questions")

    body = f'''
{C.page_hero(d["region"], d["h1"], d["lead"], trail)}

{C.trust_bar()}

<section class="section">
  <div class="wrap wrap-narrow">
    <div class="prose">{intro}</div>
  </div>
</section>

<section class="section steel">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Local knowledge</p>
      <h2>What we know about building in {name}</h2>
    </div>
    <div class="card-grid cols-3">{notes}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head head-split">
      <div>
        <p class="eyebrow">Coverage</p>
        <h2>Areas we cover</h2>
      </div>
      <p class="lead">In and around {name}, with no travel surcharge.</p>
    </div>
    <div class="card-grid cols-2">
      <div class="card reveal">
        <h3>In {name}</h3>
        <ul class="card-list">{tick_list(d["areas"])}</ul>
      </div>
      <div class="card reveal">
        <h3>Nearby</h3>
        <ul class="card-list">{tick_list(d["nearby"])}</ul>
      </div>
    </div>
  </div>
</section>

{C.service_grid(heading=f"What we do in {name}", dark=True)}

{faq_html}

{C.quote_form(f"Location: {C.plain(name)}", compact=False,
              heading=f"Get a free quote in {name}")}

{C.location_grid(exclude=slug, heading="Other areas we serve")}

{C.cta_band(f"Working on a project in {name}?",
            "Send us the details and we will get back to you, usually within one business day.")}
'''

    loc_node = C.business_node(full=False)
    loc_node.update({
        "@type": "GeneralContractor",
        "@id": f"{S.BASE}/locations/{slug}/#business",
        "name": f"{S.NAME_TEXT} — {C.plain(name)}",
        "description": C.plain(d["desc"]),
        "url": f"{S.BASE}/locations/{slug}/",
        "parentOrganization": {"@id": C.BUSINESS_ID},
        "address": {"@type": "PostalAddress",
                    "addressLocality": C.plain(name).split(" &")[0],
                    "addressRegion": S.REGION, "addressCountry": S.COUNTRY},
        "areaServed": [{"@type": "Place", "name": C.plain(a)}
                       for a in d["areas"] + d["nearby"]],
    })

    graph = [C.breadcrumb_ld(trail), loc_node, faq_ld]
    write(f"locations/{slug}/", doc(d["title"], C.plain(d["desc"]),
                                    f"locations/{slug}/", body, graph,
                                    f"/locations/{slug}/"), priority="0.8")


# ---------------------------------------------------------------------------
# About / Contact / 404
# ---------------------------------------------------------------------------

def build_about():
    trail = [("Home", "/"), ("About", "/about/")]
    values = "".join(
        f'<div class="value reveal">{C.icon(ic, "ico", 20)}<div><h3>{t}</h3><p>{b}</p></div></div>'
        for ic, t, b in VALUES)

    body = f'''
{C.page_hero("About us", "A Local Crew, Not a Call Centre",
             "We are a carpentry and renovation company based in Cornwall, working across "
             "Akwesasne and Stormont, Dundas and Glengarry.",
             trail, quote_href="/contact/")}

{C.trust_bar()}

<section class="section">
  <div class="wrap wrap-narrow">
    <div class="prose">
      <h2>Why we work the way we do</h2>
      <p class="lead">Most homeowners are not choosing between a good contractor and a bad
      one. They are choosing between four quotes with wildly different numbers and no way to
      tell what the difference actually buys.</p>
      <p>That is the problem we set out to solve in how we work. Our quotes are itemised, so
      you can see what each part of the job costs and where the money goes. We tell you what
      is likely to be behind the wall before we open it, and we carry an allowance for it
      rather than surprising you halfway through. And the people who come to your door to
      measure are the people who build the job.</p>

      <h2>Who you are dealing with</h2>
      <div class="bio reveal">
        <figure class="bio-photo">
          <picture>
            <source srcset="/assets/img/team/jake-480.webp" type="image/webp">
            <img src="/assets/img/team/jake-480.jpg"
                 alt="{S.OWNER_NAME}, the owner of {C.attr(S.SHORT)}, smiling outdoors in a
                      sunflower field with a young child on his shoulder."
                 width="240" height="240" loading="lazy" decoding="async">
          </picture>
        </figure>
        <div class="bio-intro">
          <p class="lead">Elite Carpentry is {S.OWNER_NAME}&rsquo;s business, and he is
          on the tools rather than behind a desk.</p>
          <p>He has spent close to a decade in the trade, and the range matters more
          than the number: windows, siding, fencing, decks, bathrooms and complete
          kitchen renovations. That breadth is the reason we will tell you early when a
          deck problem is really a drainage problem, or when the window you want
          replaced is fine and the trim around it is not. A crew that only does one
          thing tends to find that one thing wherever it looks.</p>
        </div>
      </div>
      <p>The work has run from single rooms in a house through to commercial projects,
      and the commercial side is where a lot of the habits come from &mdash; a schedule
      you were given in advance, a written scope everyone is working from, and a site
      left clean at the end of the day rather than at the end of the job.</p>
      <p>He is also fussy about the finish. Mitres that actually meet, fasteners in a
      line, cuts that are square because they were measured twice &mdash; the parts of a
      job nobody writes into a quote and everybody notices afterwards. When a detail
      comes out wrong it gets pulled apart and done again, not caulked over.</p>

      <h2>What licensed and insured actually means</h2>
      <p>It is the most-claimed and least-checked phrase in contracting, so here is what to
      ask for &mdash; from us, and from everyone else you are considering.</p>
      <ul>
        <li>{C.icon("tick")}<span><strong>Liability insurance.</strong> Ask for a certificate
        naming the insurer and the coverage amount. If a contractor damages your neighbour&rsquo;s
        property, this is what stands between you and the bill.</span></li>
        <li>{C.icon("tick")}<span><strong>WSIB coverage.</strong> Ask for a clearance
        certificate. If an uninsured worker is injured on your property, you can be exposed
        as the owner.</span></li>
        <li>{C.icon("tick")}<span><strong>Licensed trades for licensed work.</strong> Plumbing
        and electrical must be done by people who hold those licences. We coordinate them; we
        do not pretend to be them.</span></li>
        <li>{C.icon("tick")}<span><strong>A written contract.</strong> Scope, price, payment
        schedule and timeline in writing. Never pay the full amount up front, for any
        contractor.</span></li>
      </ul>
      <p>We will provide all of the above without being asked twice. A contractor who gets
      uncomfortable when you ask is telling you something important.</p>

      <h2>How we quote</h2>
      <p>Free, in writing, and itemised. We measure on site rather than quoting from a
      description, because the conditions are where the cost is. We check setbacks, permit
      requirements and lot coverage before we give you a number, and we tell you which
      authority the permit goes through &mdash; which around here is not always the City of
      Cornwall.</p>
      <p>If we think the job is not worth doing, or that a repair would serve you better than
      a replacement, we will say so. We would rather lose a sale than take money for work that
      does not need doing.</p>
    </div>
  </div>
</section>

<section class="section steel">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How we work</p>
      <h2>What you can hold us to</h2>
    </div>
    <div class="value-grid">{values}</div>
  </div>
</section>

{C.location_grid()}

{C.cta_band("Want to talk to us before committing to anything?",
            "That is how most of our jobs start. Call or send a note and we will tell you "
            "what your project actually involves.")}
'''
    graph = [
        C.breadcrumb_ld(trail),
        {"@type": "AboutPage", "url": f"{S.BASE}/about/",
         "name": f"About {S.NAME_TEXT}", "mainEntity": {"@id": C.BUSINESS_ID},
         "about": {"@id": C.PERSON_ID}},
        C.person_node(),
    ]
    write("about/", doc(
        "About Us | Elite Carpentry, Cornwall Ontario",
        "A licensed, insured carpentry and renovation crew based in Cornwall, Ontario. How we "
        "quote, and what licensed and insured actually means.",
        "about/", body, graph, "/about/"), priority="0.7")


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    body = f'''
{C.page_hero("Contact", "Get a Free Quote",
             "Tell us what you are planning. We reply to every inquiry, usually within one "
             "business day, and the quote is free either way.",
             trail)}

<section class="section">
  <div class="wrap">
    <div class="contact-layout">
      <div class="contact-detail">
        <h2 class="sr-head">How to reach us</h2>
        <div class="contact-item">{C.icon("phone", "ico", 20)}<div>
          <h3>Phone</h3>
          <p><a href="{S.PHONE_HREF}">{S.PHONE_DISPLAY}</a><br>
          Fastest way to reach us, especially for urgent work.</p>
        </div></div>
        <div class="contact-item">{C.icon("mail", "ico", 20)}<div>
          <h3>Email</h3>
          <p><a href="mailto:{S.EMAIL}">{S.EMAIL}</a><br>
          Send photos and measurements if you have them &mdash; it speeds up the quote.</p>
        </div></div>
        <div class="contact-item">{C.icon("clock", "ico", 20)}<div>
          <h3>Hours</h3>
          <p>{S.HOURS["display"]}<br>
          Evening and weekend site visits by arrangement.</p>
        </div></div>
        <div class="contact-item">{C.icon("pin", "ico", 20)}<div>
          <h3>Service area</h3>
          <p>Based in {S.CITY}, Ontario. Working across Akwesasne and Stormont, Dundas and
          Glengarry &mdash; no travel surcharge.</p>
        </div></div>
        <div class="contact-item">{C.icon("shield", "ico", 20)}<div>
          <h3>Licensed &amp; insured</h3>
          <p>Liability insurance and WSIB coverage. Certificates provided on request before
          work starts.</p>
        </div></div>
      </div>
      <div>
        {C.quote_form("Contact page", compact=False,
                      heading="Request your quote",
                      sub="The more detail you give us, the more accurate the first number "
                          "will be. Photos help enormously.")}
      </div>
    </div>
  </div>
</section>

{C.location_grid()}

{C.cta_band("Would rather just call?",
            "We would rather you did, honestly. It is faster than any form.",
            button="See our services")}
'''
    graph = [
        C.breadcrumb_ld(trail),
        {"@type": "ContactPage", "url": f"{S.BASE}/contact/",
         "name": f"Contact {S.NAME_TEXT}", "mainEntity": C.business_node(full=True)},
    ]
    write("contact/", doc(
        "Contact Us &amp; Free Quotes | Elite Carpentry Cornwall",
        "Request a free written quote for decks, fencing, siding, windows, bathrooms or "
        "kitchens in Cornwall and Akwesasne. We reply within one business day.",
        "contact/", body, graph, "/contact/"), priority="0.9")


def build_404():
    body = f'''
<section class="err-page">
  <div class="wrap wrap-narrow">
    <p class="code">404</p>
    <h1>That page has been taken down to the studs</h1>
    <p class="lead">The link you followed does not lead anywhere. Here is where to go instead.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/">Back to home{C.icon("arrow")}</a>
      <a class="btn btn-ghost" href="/services/">See our services</a>
    </div>
  </div>
</section>
'''
    html = (C.head("Page not found | Elite Carpentry",
                   "That page could not be found.", "404.html", None, noindex=True)
            + C.header("") + f'<main id="main">{body}</main>' + C.footer(minimal=True))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(relativize(html, 0))
    print("  /404.html")


# ---------------------------------------------------------------------------
# Non-HTML files
# ---------------------------------------------------------------------------

def build_meta_files():
    lastmod = "2026-08-12"
    urls = "\n".join(
        f"  <url>\n    <loc>{S.BASE}/{p}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n"
        f"    <priority>{pr}</priority>\n  </url>"
        for p, pr, cf in PAGES)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}\n</urlset>\n")
    _put("sitemap.xml", sitemap)

    _put("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S.BASE}/sitemap.xml\n")

    _put("site.webmanifest", json.dumps({
        "name": S.NAME_TEXT,
        "short_name": S.SHORT,
        "description": C.plain(S.TAGLINE),
        "start_url": "./",
        "display": "standalone",
        "background_color": "#0B0B0C",
        "theme_color": "#0B0B0C",
        "icons": [
            {"src": "assets/img/android-chrome-192x192.png", "sizes": "192x192",
             "type": "image/png"},
            {"src": "assets/img/android-chrome-512x512.png", "sizes": "512x512",
             "type": "image/png"},
        ],
    }, indent=2) + "\n")


def _put(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  /{name}")


# ---------------------------------------------------------------------------

def main():
    print("Building pages:")
    build_home()
    build_services_hub()
    for slug in S.SERVICE_SLUGS:
        build_service(slug)
    build_locations_hub()
    for slug in S.LOCATION_SLUGS:
        build_location(slug)
    build_about()
    build_contact()
    build_404()
    build_meta_files()

    print(f"\n{len(PAGES)} pages in sitemap, plus 404.html.")

    if SEO_WARNINGS:
        print(f"\nSEO length warnings ({len(SEO_WARNINGS)}):")
        for w in SEO_WARNINGS:
            print("  !", w)
    else:
        print("Titles and meta descriptions are all within search-result limits.")

    if S.PLACEHOLDERS:
        print("\n" + "!" * 72)
        print("PLACEHOLDERS STILL IN THE BUILD — the site must not go live like this:")
        for k, v in S.PLACEHOLDERS.items():
            print(f"  {k:<16} {v}")
        print("See NOTES.local.md -> Launch checklist.")
        print("!" * 72)
    else:
        # No fake values left. That is NOT the same as ready to launch — the
        # checklist still has items a build cannot see (a live form test, the
        # domain, the insurance claim), so say what was actually checked.
        print("\nNo placeholders left in the build.")
        print(f"  Form posts to {S.FORM_ACTION}")
        print(f"  Leads go to    {S.FORM_RECIPIENT}")
        print("  Still manual: send a real test through the live form and confirm it")
        print("  arrives (check junk) — a misconfigured endpoint fails silently.")
        print("  See NOTES.local.md -> Launch checklist for what else is outstanding.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
