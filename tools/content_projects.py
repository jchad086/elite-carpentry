#!/usr/bin/env python3
"""
The owner's real project photos — the portfolio on the home page.

THESE ARE THE COMPANY'S OWN WORK, unlike the licensed stock in
assets/img/photos/. That is the whole distinction, and it decides how they may
be described:

  - Real work  -> may be captioned as theirs ("Raised pressure-treated deck...")
  - Stock      -> descriptive alt text only, never attributive

What must still NOT be invented: the town, the client, the date, the price, or
the product brand. None of that was supplied with the photos, so none of it
appears here. Every line below describes only what is visible in the frame.
Verified by looking at each image, not by trusting the filename.

Masters live in assets/img/photos/originals/; run tools/project-photos.py to
regenerate the web-sized derivatives in assets/img/projects/.

Keys:
  slug        matches the master filename in originals/ (any extension)
  tag         short label on the carousel slide
  caption     one attributive sentence — only what is in the frame
  alt         descriptive, for a reader who cannot see the photo
  href, link  where the slide's arrow link goes
  focus       vertical crop centre, 0 = top of frame, 1 = bottom (default 0.35)
  focus_wide  same, for the 16:10 cut, when it wants a different band
  focus_x     horizontal crop centre, for landscape masters cut to portrait
  service     if set, this photo replaces the stock figure on that service page
  letterboxed set on screenshots so the black bars get trimmed first

ORDER MATTERS: this list is the carousel order. Strongest frame first — it is
the only one most visitors will see.
"""

PROJECTS = [
    {
        "slug": "porch-screened",
        "tag": "Screened porch",
        "caption": "Screened porch with a herringbone skirt, scrolled brackets and a "
                   "matching open deck alongside.",
        "alt": "A cedar-toned screened porch with a shingled roof, decorative scrolled "
               "corner brackets and skirting laid in a herringbone pattern, with wide "
               "stairs and an adjoining open deck with black aluminum balusters.",
        "href": "/services/decks/",
        "link": "See our deck work",
        "focus": 0.30,
        "focus_wide": 0.36,
        "service": "decks",
    },
    {
        "slug": "deck-alum",
        "tag": "Deck build",
        "caption": "Raised deck with black aluminum railings, full-width stairs and "
                   "vertical board skirting.",
        "alt": "A raised pressure-treated deck against a bungalow, with black aluminum "
               "railings, a wide flight of stairs railed on both sides and vertical "
               "board skirting below the deck frame.",
        "href": "/services/decks/",
        "link": "See our deck work",
        "focus": 0.34,
    },
    {
        "slug": "veranda-brick",
        "tag": "Front veranda",
        "caption": "Front veranda with black aluminum railing, mitred cap and vertical "
                   "board skirting.",
        "alt": "A pressure-treated front veranda on a red brick bungalow, with a black "
               "aluminum railing, a wide mitred wooden cap and vertical board skirting, "
               "and stairs railed to match.",
        "href": "/services/decks/",
        "link": "See our deck work",
        "focus": 0.40,
        "focus_wide": 0.46,
    },
    {
        "slug": "bathroom-tub",
        "tag": "Bathroom renovation",
        "caption": "Bathroom with a tiled tub surround, matte black fixtures and a "
                   "stone-topped vanity.",
        "alt": "A renovated bathroom with a marble-look subway tiled tub surround, matte "
               "black shower fittings, a dark shaker vanity with a stone top, a tall "
               "linen cabinet and pale wood-look plank flooring.",
        "href": "/services/bathroom-renovations/",
        "link": "See our bathroom work",
        "focus": 0.5,
        # High: the 16:10 band is shallow, and centring it puts the toilet in
        # the middle of the frame. 0.24 lands on the tile, the fixtures and the
        # window instead, with the toilet at the bottom edge.
        "focus_wide": 0.24,
        "service": "bathroom-renovations",
        "letterboxed": True,
    },
    {
        "slug": "deck2",
        "tag": "Deck build",
        "caption": "Composite decking with a picture-framed border and matching "
                   "aluminum railing.",
        "alt": "A composite deck surface in warm brown boards with a picture-framed "
               "border, black aluminum railings and stairs descending at one corner.",
        "href": "/services/decks/",
        "link": "See our deck work",
    },
    {
        "slug": "hearth-shiplap",
        "tag": "Finish carpentry",
        "caption": "Stove alcove in shiplap with a capped ledge and a mitred tile "
                   "hearth.",
        "alt": "A corner stove alcove finished in white shiplap with a black capped "
               "ledge running around it, a tiled hearth pad edged in mitred white trim, "
               "and a black stove with the fire lit.",
        "href": "/contact/",
        "link": "Ask about finish carpentry",
        "focus": 0.42,
        "focus_wide": 0.55,
    },
    {
        "slug": "kitchen-counter",
        "tag": "Kitchen renovation",
        "caption": "New counter, sink and tiled backsplash going in over the existing "
                   "cabinets.",
        "alt": "A kitchen mid-renovation with a newly fitted wood-look laminate counter, "
               "a stainless steel sink and chrome faucet, and a blue-grey subway tile "
               "backsplash above white cabinets.",
        "href": "/services/kitchen-renovations/",
        "link": "See our kitchen work",
        "focus": 0.45,
        "focus_wide": 0.36,
        "service": "kitchen-renovations",
    },
    {
        "slug": "porch-roof",
        "tag": "Covered porch",
        "caption": "Covered front porch with a shed roof carried on timber posts, over a "
                   "railed landing and steps.",
        "alt": "A pressure-treated front porch with a shed-style roof carried on two "
               "timber posts, black aluminum balusters between wooden rails, board "
               "skirting and open steps down to the driveway.",
        "href": "/services/decks/",
        "link": "See our deck work",
        "focus": 0.38,
        "focus_wide": 0.44,
    },
    {
        "slug": "deck3",
        "tag": "Finish carpentry",
        "caption": "Built-in storage bench in grey composite, with mitred lids and a "
                   "privacy screen.",
        "alt": "A grey composite deck with a built-in storage bench, mitred "
               "picture-frame lids and a black decorative privacy screen against "
               "cream siding.",
        "href": "/services/decks/",
        "link": "See our deck work",
    },
]

# Masters in originals/ that are deliberately NOT published, and why. Kept so
# the next person does not "helpfully" add them back without knowing.
#
#   basement-room   an empty grey corner. The baseboard and window casing are
#                   genuinely theirs, but the frame sells nothing.
#   patio-timber    paver patio with a timber curb and wood retaining walls.
#                   Good work, but it is hardscaping, and the frame is busy
#                   with a materials pile and the photographer's shadow.
#   deck-framing    a deck part-built, with ladders and offcuts. Honest and
#                   useful for a "how we build" slot, but there is no such slot
#                   on the site today.
#   porch-deck      a second angle of the porch-screened job. Strong photo,
#                   held back only so one job does not take two carousel slots.
#   deck1           the SAME FRAME as deck-alum, at 1536x2048 against the
#                   original's 4284x5712 — a phone-shared copy of the same
#                   photo. Publishing both would have shown one job twice in
#                   one carousel. deck-alum is kept because it is the master.
UNUSED = ("basement-room", "patio-timber", "deck-framing", "porch-deck", "deck1")
