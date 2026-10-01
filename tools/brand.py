#!/usr/bin/env python3
"""
Single source of truth for every fact about the business that appears on more
than one page: name, phone, email, service list, location list, nav structure.

Nothing else in the repo should hard-code a phone number or a service name. If
you need to change the company's number, change PHONE_DISPLAY / PHONE_E164 here
and re-run `python3 tools/build.py`.

PLACEHOLDERS: values wrapped in the PLACEHOLDERS dict below are not real. The
build prints a loud warning listing every one of them, and the site must not go
live until they are replaced. The launch checklist lives in NOTES.local.md,
which is not in the public repo.
"""

# --- Identity ---------------------------------------------------------------

NAME = "Elite Carpentry &amp; Renovations"      # HTML-escaped, for markup
NAME_TEXT = "Elite Carpentry & Renovations"     # plain, for JSON-LD and titles
SHORT = "Elite Carpentry"
TAGLINE = "Decks, fences, siding, windows, kitchens and baths built to last in Cornwall and Akwesasne."

BASE = "https://www.elite-carpentry.ca"
LOCALE = "en-CA"

# --- The owner ---------------------------------------------------------------
# Used by the Person node in the JSON-LD and by /about/. The full name appears
# once in visible copy on /about/ and everything after it is "Jake" — structured
# data is supposed to mirror what a reader can actually see on the page, so the
# schema must never be the only place the surname exists.
OWNER_NAME = "Jake Martin"
OWNER_FIRST = "Jake"

# Jake OWNS the company — he is not staff. schema.org has no Organization ->
# Person "owner" property (the vocabulary offers founder, employee, member and
# nothing else), so the business node links to him with `founder`, which is the
# standard idiom for an owner-operator and the only one that does not read as
# "works here". `employee` would actively misrepresent him.
OWNER_ROLE = "Owner"

# --- Contact -----------------------------------------------------------------
# Real values, confirmed by the owner 2026-08-13. Every phone number and email
# address on the site comes from here — the only other numbers in the codebase
# are the municipal building departments quoted in page copy, which are
# deliberately different and must not be changed to these.

PHONE_DISPLAY = "(343) 370-4191"
PHONE_E164 = "+1-343-370-4191"
PHONE_HREF = "tel:+13433704191"

# The published address, and the address the Formspree form should deliver to.
# Moved onto the domain 2026-09-30, once elite-carpentry.ca had a mailbox —
# earlier addresses sat on a domain with no mail routing, which is why the site
# ran on webmail until now. Confirmed by the owner as live and tested.
EMAIL = "jake@elite-carpentry.ca"

CITY = "Cornwall"
REGION = "ON"
REGION_NAME = "Ontario"
COUNTRY = "CA"

# Confirmed by the owner 2026-08-17. Drives the visible hours on /contact/ and
# the openingHoursSpecification in the JSON-LD, so the two can never disagree.
HOURS = {
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "07:00",
    "closes": "17:00",
    "display": "Monday to Friday, 7:00am – 5:00pm",
}

# Social / directory profiles. Empty until the owner has them; `sameAs` is
# omitted from JSON-LD rather than shipped empty.
SAME_AS = []

# Anything still fake at build time. Emptied 2026-08-17 when the real Formspree
# ID landed. build.py reads this and refuses to stay quiet while it has entries.
PLACEHOLDERS = {}

# --- Formspree --------------------------------------------------------------
# This site needs its OWN form ID. Reusing another site's endpoint routes this
# client's leads into someone else's inbox. main.js detects the placeholder and
# shows the error state rather than silently dropping a lead.
#
# None of this can be set from here: where the form delivers lives in the
# Formspree dashboard, not in this repo. Editing EMAIL above changes what the
# site PUBLISHES and nothing else.
#
# ⚠️ CHANGING THE DELIVERY ADDRESS (the situation on 2026-09-30):
#   1. formspree.io -> form FORMSPREE_ID below -> set recipient to
#      FORM_RECIPIENT, exactly.
#   2. Open the verification email Formspree sends to the NEW address and click
#      it. Until that happens Formspree keeps delivering to the old recipient,
#      with no error anywhere — the site advertises one address while leads
#      arrive at another.
#   3. Submit the live form and confirm it lands. Check spam: providers filter
#      form relays, and a quote request in a spam folder is a lost customer who
#      thinks they were ignored.
#   4. Mark formspree.io a safe sender in the receiving mailbox.
#
# STARTING FROM SCRATCH instead: sign in at formspree.io, create a form with
# FORM_RECIPIENT as the recipient, do step 2, then copy the xxxxxxxx out of
# https://formspree.io/f/xxxxxxxx into FORMSPREE_ID and rebuild.
#
# FORM_RECIPIENT is recorded here so the destination is unambiguous, and so it
# is obvious if it ever drifts from the address published on the site. It is
# only a record of intent — it does not configure anything.
FORM_RECIPIENT = EMAIL
FORMSPREE_ID = "xzepjyvz"       # supplied 2026-08-17; recipient repointed 2026-09-30
FORM_ACTION = f"https://formspree.io/f/{FORMSPREE_ID}"
FORM_SUBJECT = "New quote request — Elite Carpentry"

# --- Trust claims -----------------------------------------------------------
# ONLY claims the owner has confirmed. Warranty terms, fixed-price guarantees,
# review counts and years-in-business are deliberately absent until he confirms
# real numbers — an unverifiable claim on a trust-led site is worse than none.
# CONFIRMED by the owner 2026-08-17: he is licensed, insured and WSIB covered.
# This claim appears on every page of the site, and /about/ invites visitors to
# ask for the certificates — so it has to stay true. If coverage ever lapses,
# this list is the first thing to change.
TRUST_POINTS = [
    ("shield", "Licensed &amp; fully insured", "WSIB coverage on every job site."),
    ("pin", "Cornwall &amp; Akwesasne", "Local crews, not a franchise call centre."),
    ("quote", "Free written quotes", "Detailed, itemised, no obligation."),
]

# --- Services ---------------------------------------------------------------
# slug, nav label, short label, one-line blurb for cards.

SERVICES = [
    ("decks", "Decks", "Deck building",
     "Custom pressure-treated, cedar and composite decks engineered for Eastern Ontario frost."),
    ("fencing", "Fencing", "Fence installation",
     "Privacy, picket, PVC, aluminum and chain link — set deep, set straight, set square."),
    ("siding", "Siding", "Siding installation",
     "Vinyl, engineered wood and board-and-batten, with soffit, fascia and eavestrough."),
    ("windows", "Windows", "Window replacement",
     "ENERGY STAR windows and doors installed to spec, air-sealed and properly flashed."),
    ("bathroom-renovations", "Bathrooms", "Bathroom renovations",
     "Full gut-and-rebuild bathrooms, tub-to-shower conversions and accessible walk-ins."),
    ("kitchen-renovations", "Kitchens", "Kitchen renovations",
     "Layout changes, custom cabinetry, islands and finish carpentry done by one crew."),
]

SERVICE_SLUGS = [s[0] for s in SERVICES]


def service(slug):
    for s in SERVICES:
        if s[0] == slug:
            return s
    raise KeyError(slug)


# --- Locations --------------------------------------------------------------
# slug, display name, short nav name.

LOCATIONS = [
    ("cornwall", "Cornwall", "Cornwall"),
    ("akwesasne", "Akwesasne", "Akwesasne"),
    ("long-sault", "Long Sault", "Long Sault"),
    ("ingleside", "Ingleside", "Ingleside"),
    ("lancaster-glen-walter", "Lancaster &amp; Glen Walter", "Lancaster"),
    ("alexandria", "Alexandria", "Alexandria"),
]

LOCATION_SLUGS = [l[0] for l in LOCATIONS]

# Plain-text names for JSON-LD areaServed on the business node.
AREA_SERVED = [
    "Cornwall", "Akwesasne", "Long Sault", "Ingleside", "Lancaster",
    "Glen Walter", "Alexandria", "Williamstown", "Martintown",
    "Summerstown", "South Stormont", "South Glengarry",
]
