#!/usr/bin/env python3
"""
Per-service page content.

Copy is written per service, not templated. Six near-identical pages with the
service name swapped is exactly what Google discounts, and it would not convert
either. Every page carries specifics a Cornwall homeowner can check: the City's
own permit thresholds, Ontario One Call, the Home Renovation Savings window,
Ontario Building Code requirements.

FACT-CHECK BEFORE LAUNCH — every figure below is sourced but should be
re-verified with the City of Cornwall Building Division (613) 930-2787 and the
current program pages, since by-laws and rebate windows change:
  - Deck permit threshold and guard/footing specs: City of Cornwall DECK-GUIDE-2026.pdf
  - Home Renovation Savings: $100 per eligible ENERGY STAR opening, to 2026-11-30,
    claimable only through a registered Participating Contractor.
    *** The copy below is written to be true whether or not the contractor is
    a registered Participating Contractor. Do not change it to imply he is
    without confirming first — see NOTES.local.md. ***
"""

SERVICES = {}

# Section imagery for the pages still running on STOCK: slug -> (basename, alt).
#
# A service page uses a real job photo the moment one exists — see the `service`
# key in tools/content_projects.py, which is what decks, bathrooms and kitchens
# now run on. This table is only the fallback, and every entry left in it is a
# licensed Unsplash photograph, NOT this company's work.
#
# So the alt text here is descriptive ("a wooden privacy fence with a lattice
# topper") and never attributive ("a fence we built in Cornwall"), and these
# figures carry no caption. Captioning stock as their own work would destroy the
# trust this site exists to build.
#
# Fetched and optimised by tools/fetch-photos.py; credits in the photos folder.
# DELETE the entry, and the file, as soon as a real photo covers that service.
PHOTOS = {
    "fencing": ("fence",
                "A wooden privacy fence with a lattice topper and a diagonally braced gate"),
    "siding": ("siding",
               "A two-storey house clad in grey lap siding with white trim and a "
               "cedar-shingled gable"),
    # Replaced 2026-08-17. The previous shot was of flaking, half-rotten sashes —
    # the problem, not the result. On a page selling window replacement the
    # reader associates whatever is in the frame with the contractor, so the
    # photo has to show a house someone would want to end up with.
    "windows": ("windows",
                "A dark green clapboard house with white-trimmed double-hung windows, a "
                "covered front porch and a magnolia in bloom"),
}


def _add(d):
    SERVICES[d["slug"]] = d


# --- Decks ------------------------------------------------------------------

_add({
    "slug": "decks",
    "nav": "Decks",
    "h1": "Deck Builders in Cornwall, Ontario",
    "title": "Deck Builders in Cornwall, Ontario | Elite Carpentry",
    "desc": ("Custom deck builders in Cornwall, Akwesasne and SD&G. Pressure-treated, cedar "
             "and composite decks built to Code, with the permit handled. Free quotes."),
    "eyebrow": "Deck building",
    "service_type": "Deck building",
    "lead": ("Pressure-treated, cedar and composite decks engineered for Eastern Ontario "
             "frost &mdash; footings dug to the depth the City requires, not the depth that "
             "is quick."),
    "intro": [
        ("A deck in this part of Ontario has to survive a 30-degree summer afternoon and a "
         "&minus;30 January night, and it is the freeze-thaw cycle that kills them. When "
         "footings are not below the frost line, the ground lifts them every spring. Two or "
         "three winters later the ledger is racked, the stairs no longer meet the landing, "
         "and the guard has gone loose."),
        ("That is the single most common failure we get called to fix, and it is entirely "
         "avoidable. We dig every footing to the depth the City of Cornwall Building "
         "Division requires for our area, pour proper concrete pads rather than dropping "
         "blocks on sod, and flash the ledger so water is directed away from your rim joist "
         "instead of into it."),
    ],
    "items_head": "What a deck build includes",
    "items": [
        ("Design and layout",
         "We measure on site, check your setbacks and lot coverage, and lay the deck out "
         "around how you actually use the yard &mdash; where the sun lands at 6pm, where the "
         "barbecue goes, where the door swings."),
        ("Permit drawings and application",
         "If your deck needs a permit we prepare the drawings and file the application with "
         "the City. You are not left figuring out framing plans and site plans on your own."),
        ("Footings below frost",
         "Concrete footings sized and poured to Code, dug to the depth required for Eastern "
         "Ontario. This is the part nobody sees and the only part that determines whether "
         "the deck is still square in ten years."),
        ("Framing, decking and stairs",
         "No.2 grade or better framing lumber, joists at the spacing your decking product "
         "calls for, hidden fasteners on composite, and stairs with consistent rise and run "
         "&mdash; uneven treads are both a Code problem and a trip hazard."),
        ("Guards and railings",
         "Built to the Code height with the required maximum opening between balusters, so "
         "the deck passes inspection and is safe for kids and dogs."),
        ("Cleanup and final inspection",
         "Site cleared, offcuts and packaging removed, and we meet the inspector so you do "
         "not have to book a day off work."),
    ],
    "options_head": "Decking materials, and what we would actually tell you",
    "options_intro": ("There is no single right answer here. The honest version of the "
                      "trade-off looks like this:"),
    "options": [
        ("Pressure-treated",
         "The lowest up-front cost and still the most common deck in Cornwall. It will need "
         "cleaning and re-sealing every two to three years, and boards will cup or check "
         "over time. Choose it if budget is the deciding factor and you do not mind the "
         "maintenance weekend.",
         ["Lowest material cost", "Widely available locally", "Needs regular sealing"]),
        ("Cedar",
         "Naturally rot-resistant, noticeably nicer underfoot and it smells like a deck "
         "should. Softer than pressure-treated, so it marks more easily. Left unfinished it "
         "weathers to silver-grey; sealed, it holds its colour.",
         ["Warm appearance", "Naturally rot-resistant", "Softer surface, marks easier"]),
        ("Composite and PVC",
         "The highest up-front cost and the lowest ongoing one &mdash; no sanding, no "
         "staining, and it will not splinter. Worth doing properly: composite needs the "
         "joist spacing the manufacturer specifies, and picture-frame edges need blocking. "
         "Done wrong it sags between joists and the warranty is void.",
         ["No staining or sealing", "25&ndash;50 year product warranties common",
          "Requires correct joist spacing"]),
    ],
    "callout": ("Do you need a permit for a deck in Cornwall?",
                "<p>Under the City of Cornwall&rsquo;s deck guidelines, a deck more than "
                "<strong>60&nbsp;cm above grade</strong> requires a building permit. A deck at "
                "or near grade that is <strong>freestanding</strong> &mdash; not attached to the "
                "house &mdash; generally does not. Permit fees typically run in the "
                "<strong>$198&ndash;$600</strong> range depending on size.</p>"
                "<p>Guards are required once you are more than 60&nbsp;cm up, at a minimum "
                "height of <strong>1.07&nbsp;m</strong>, with openings no greater than "
                "<strong>100&nbsp;mm</strong>. Zoning by-laws also cap how much of your lot can "
                "be covered; going over means a minor variance from the Committee of "
                "Adjustment.</p>"
                "<p>We confirm the current requirements and fee schedule with the Building "
                "Division at <a href=\"tel:+16139302787\">(613)&nbsp;930-2787</a> on every "
                "job, and we file the application for you. Rules do change &mdash; check the "
                "City&rsquo;s current deck guide before relying on these figures.</p>"),
    "faqs": [
        ("Do I need a building permit to build a deck in Cornwall?",
         "<p>If the deck surface sits more than 60 cm above the ground, yes. A freestanding "
         "deck at or near grade that is not attached to the house generally does not need "
         "one. Fees usually fall between $198 and $600 depending on the size of the "
         "structure. We prepare the drawings and file the application as part of the job, "
         "and we confirm the current thresholds with the City's Building Division before "
         "quoting, because by-laws change.</p>"),
        ("How deep do deck footings have to go in Cornwall?",
         "<p>Below the local frost line, which in Eastern Ontario is deeper than the "
         "1.2 m figure often quoted for southern Ontario. We confirm the required depth "
         "with the City for your specific address rather than working from a rule of thumb. "
         "Footings also have a minimum size and thickness under the Ontario Building Code, "
         "and the concrete has a minimum strength. Skipping any of this is why decks heave.</p>"),
        ("What does a new deck cost?",
         "<p>It depends on four things: total square footage, height off the ground, the "
         "decking material, and how much railing and stair work is involved. Height matters "
         "more than people expect &mdash; a second-storey deck needs deeper footings, taller "
         "posts, more bracing and a longer stair run, so it can cost substantially more per "
         "square foot than a ground-level deck of the same size. We quote in writing and "
         "itemised, so you can see exactly what is driving the number.</p>"),
        ("Composite or pressure-treated &mdash; which should I choose?",
         "<p>If you want the lowest up-front cost, pressure-treated. If you want to stop "
         "staining decks on summer weekends, composite. Composite costs more to install as "
         "well as to buy, because it needs tighter joist spacing and blocking at "
         "picture-frame edges, but most product warranties run 25 to 50 years. Cedar sits "
         "in the middle and looks the best of the three when it is new.</p>"),
        ("Can you repair or resurface my existing deck instead of replacing it?",
         "<p>Often, yes &mdash; and it is worth asking. If the footings and framing are sound, "
         "replacing just the decking boards and railings costs far less than a full rebuild. "
         "What we check first is the ledger connection, the footings, and the joists at the "
         "ends where water sits. If the frame has moved or the ledger was never flashed, "
         "resurfacing is money spent on a structure that is already failing.</p>"),
    ],
})

# --- Fencing ----------------------------------------------------------------

_add({
    "slug": "fencing",
    "nav": "Fencing",
    "h1": "Fence Installation in Cornwall, Ontario",
    "title": "Fence Installation Cornwall, Ontario | Elite Carpentry",
    "desc": ("Fence installation in Cornwall, Akwesasne and SD&G. Privacy, cedar, PVC, "
             "aluminum and chain link, posts set below frost, locates arranged."),
    "eyebrow": "Fence installation",
    "service_type": "Fence installation",
    "lead": ("Privacy, picket, PVC, aluminum and chain link &mdash; set deep, set straight, "
             "and set on the right side of your property line."),
    "intro": [
        ("Two things sink a fence job, and neither of them is the fence. The first is post "
         "depth: posts that do not reach below frost will lift, and once one post lifts the "
         "whole run goes out of line. The second is the property line &mdash; a fence built "
         "even a few inches over is a legal problem between neighbours long after the "
         "contractor has gone."),
        ("So we start with the boundary and the by-law, not the panels. We work from your "
         "survey where you have one, we arrange the underground locates that Ontario law "
         "requires before anyone puts a post hole in the ground, and we check the City's "
         "fence by-law for the height limits that apply to your yard &mdash; they are not the "
         "same in a front yard as they are in a back yard."),
    ],
    "items_head": "How we install a fence",
    "items": [
        ("Boundary and by-law check",
         "We confirm where your line actually runs and what height is permitted for that "
         "part of your lot before we quote, so nothing has to come down later."),
        ("Underground locates",
         "Locates are free and legally required in Ontario before digging. We place the "
         "request through Ontario One Call and wait for the clearance before a single hole "
         "is dug."),
        ("Posts set below frost",
         "Holes augered below the frost line and set in concrete, spaced for the panel "
         "system so runs stay straight and gates keep their swing."),
        ("Gates that still work in year five",
         "Properly braced gate posts, adjustable hinges, and hardware rated for the gate "
         "weight. A sagging gate is almost always an under-built gate post."),
        ("Grade following or stepping",
         "On sloped yards we will show you the difference between racking the fence to "
         "follow the ground and stepping it down in panels, and what each one looks like "
         "when it is finished."),
        ("Cleanup and spoil removal",
         "Auger spoil, offcuts and old fencing hauled away. Your yard goes back to being a "
         "yard the same day we finish."),
    ],
    "options_head": "Fence types we install",
    "options_intro": "Matched to what the fence is actually for &mdash; privacy, containment, or looks.",
    "options": [
        ("Wood privacy and cedar",
         "Board-on-board, shadow-box and standard privacy in pressure-treated or cedar. The "
         "most private and the most customisable, and the option that takes the most "
         "maintenance. Cedar holds up longest without treatment.",
         ["Full privacy", "Any height the by-law allows", "Stain or leave to weather"]),
        ("PVC and vinyl",
         "No painting, no staining, no rot. Costs more up front than wood and cannot be "
         "modified on site the way wood can, but it looks the same in year twelve as it did "
         "on day one.",
         ["Effectively zero maintenance", "Colour-fast", "Higher up-front cost"]),
        ("Aluminum and ornamental",
         "For pool enclosures, front yards and anywhere you want a boundary without losing "
         "the view. Powder-coated aluminum will not rust and is light enough to span uneven "
         "ground cleanly.",
         ["Pool-code compliant options", "Will not rust", "Keeps sightlines open"]),
        ("Chain link and farm fence",
         "The most cost-effective way to enclose a large area or contain a dog. Galvanised "
         "or black vinyl-coated, with privacy slats if you want the screening without the "
         "cost of a board fence.",
         ["Lowest cost per foot", "Ideal for large yards", "Slats available for privacy"]),
    ],
    "callout": ("Before anyone digs: locates are the law",
                "<p>In Ontario you must have underground utilities located before digging &mdash; "
                "including for fence posts. The service is free and is requested through "
                "<strong>Ontario One Call</strong>. Hitting a gas line or a buried service is "
                "dangerous and expensive, and the liability lands on whoever dug.</p>"
                "<p>We place the locate request and wait for clearance on every job. If a "
                "fence contractor offers to start tomorrow without mentioning locates, that "
                "is the moment to ask why.</p>"),
    "faqs": [
        ("How tall can my fence be in Cornwall?",
         "<p>The City's fence by-law sets maximum heights, and they differ between front "
         "yards and rear or side yards &mdash; front yard limits are lower, because of sightlines "
         "at driveways and corners. Pool enclosures have their own separate requirements. We "
         "check the current by-law against your specific lot before quoting rather than "
         "assuming, since the limits are also affected by corner lots and by whether the "
         "fence sits on a retaining wall.</p>"),
        ("Do I need a survey before you build?",
         "<p>Not always, but it is the safest thing you can bring us. If you have a survey "
         "we work from it. If you do not, we can work from visible boundary evidence and "
         "existing pins, but the risk of an encroachment sits with the property owner, so "
         "for a contested or tight boundary we would rather you get it surveyed than guess. "
         "It costs far less than moving a finished fence.</p>"),
        ("How deep do fence posts need to be?",
         "<p>Below the frost line for our area, set in concrete. Shallow posts are the "
         "single most common cause of a fence going crooked, and it usually shows up in the "
         "second or third spring. Gate posts get extra depth and bracing, because they carry "
         "a swinging load that the rest of the run does not.</p>"),
        ("Do I have to tell my neighbour?",
         "<p>You are not obliged to, but we would. If the fence sits on the shared line, "
         "Ontario's Line Fences Act contemplates the cost being shared, and a conversation "
         "before the posts go in prevents a dispute afterwards. If you would rather avoid "
         "the discussion entirely, we can build the fence fully inside your own property "
         "line instead.</p>"),
        ("Can you install a fence on a sloped or uneven yard?",
         "<p>Yes. There are two approaches: racking, where the panels follow the slope and "
         "the pickets stay vertical, and stepping, where each panel stays level and steps "
         "down, leaving triangular gaps at the bottom. Racking looks cleaner on a gentle "
         "grade; stepping suits a steeper one and some panel systems only allow one or the "
         "other. We will show you both before you decide.</p>"),
    ],
})

# --- Siding -----------------------------------------------------------------

_add({
    "slug": "siding",
    "nav": "Siding",
    "h1": "Siding Contractors in Cornwall, Ontario",
    "title": "Siding Contractors Cornwall, Ontario | Elite Carpentry",
    "desc": ("Siding installation in Cornwall, Akwesasne and SD&G. Vinyl, engineered wood "
             "and board-and-batten, plus soffit, fascia and eavestrough. Free quotes."),
    "eyebrow": "Siding installation",
    "service_type": "Siding installation",
    "lead": ("Vinyl, engineered wood and board-and-batten &mdash; with the house wrap, flashing "
             "and ventilation details that decide whether the wall behind it stays dry."),
    "intro": [
        ("Siding is the most visible thing you can do to a house and the easiest to do "
         "badly, because almost all of the work that matters is hidden the moment the last "
         "panel goes on. What keeps a wall dry is not the siding &mdash; it is the weather "
         "barrier behind it, the flashing above every window and door, and the drainage path "
         "water takes when it inevitably gets past the surface."),
        ("A lot of the housing stock around here is now well past the service life of its "
         "original cladding. Long Sault and Ingleside were built in 1957 and 1958 to rehouse "
         "families displaced by the St. Lawrence Seaway, and much of Cornwall's east end is "
         "the same vintage. On houses that age we routinely open the wall and find no "
         "weather barrier at all, or flashing that was never installed over the window "
         "heads. Re-siding is the one chance you get to fix that."),
    ],
    "items_head": "What a re-side involves",
    "items": [
        ("Tear-off and inspection",
         "Old cladding comes off and we look at what is underneath before anything goes back "
         "on. Rotten sheathing, damaged studs and previous water damage get photographed and "
         "shown to you, not quietly covered up."),
        ("Sheathing repairs",
         "Any compromised sheathing is replaced. We price this as a per-sheet allowance up "
         "front so there is no uncomfortable conversation halfway through the job."),
        ("Weather barrier",
         "House wrap installed properly &mdash; correct overlaps, taped seams, and integrated "
         "with the window flashing so water running down the wall is shed outward rather "
         "than behind it."),
        ("Flashing and trim",
         "Head flashing over windows and doors, proper J-channel and corner detail, and "
         "kick-out flashing where a roof meets a wall. That last one is small, cheap, and "
         "the source of an enormous share of hidden wall rot."),
        ("Siding installation",
         "Fastened to the manufacturer's spec &mdash; vinyl hung, not nailed tight, so it can "
         "expand and contract through a 60-degree annual temperature swing without buckling."),
        ("Soffit, fascia and eavestrough",
         "Vented soffit sized for the attic it serves, fascia that carries the trough "
         "properly, and eavestrough with the fall and downspout placement to move water away "
         "from your foundation."),
    ],
    "options_head": "Cladding options",
    "options_intro": "What each one is genuinely good at.",
    "options": [
        ("Vinyl siding",
         "The most common choice in Cornwall for good reason: the lowest installed cost, no "
         "painting, and a large colour range. Modern insulated vinyl also adds a little "
         "R-value and lies noticeably flatter than the standard product.",
         ["Lowest installed cost", "No painting", "Insulated options available"]),
        ("Engineered wood",
         "Looks like painted wood with far more dimensional stability and impact resistance "
         "than vinyl. It is the right call on a house where vinyl would look wrong, and it "
         "handles a stray hockey puck considerably better.",
         ["Authentic wood appearance", "Strong impact resistance", "Pre-finished options"]),
        ("Board-and-batten",
         "Vertical boards with battens over the seams. It suits farmhouse and modern-rustic "
         "elevations and works particularly well as an accent on gables and entry walls "
         "rather than over an entire house.",
         ["Strong architectural character", "Excellent as an accent", "Vinyl or engineered wood"]),
    ],
    "callout": ("Why kick-out flashing matters more than the siding you pick",
                "<p>Where a roof edge runs into a wall, water needs somewhere to go. Without a "
                "small piece of kick-out flashing directing it into the eavestrough, it runs "
                "straight down behind the cladding and into the wall cavity &mdash; every rainfall, "
                "for years, with nothing visible from outside.</p>"
                "<p>By the time it shows up inside as a stain, the sheathing and framing behind "
                "it are usually gone. It is a small detail and it costs almost nothing to do "
                "at install time. We do it as standard, and we check for it on every re-side "
                "we open up.</p>"),
    "faqs": [
        ("How long does vinyl siding last in Eastern Ontario?",
         "<p>Typically 25 to 40 years, though our climate is harder on it than most: "
         "ultraviolet in summer, and cold that makes vinyl brittle enough to crack on impact "
         "in deep winter. Installation quality matters as much as product quality. Vinyl "
         "that is nailed tight instead of hung with room to move will buckle in the first "
         "hot spell, and no warranty covers that.</p>"),
        ("Can you side over the existing siding?",
         "<p>Sometimes it is physically possible, but we usually advise against it. Going "
         "over the top means you never see the sheathing, never confirm there is a weather "
         "barrier, and never correct missing window flashing &mdash; which are the three things "
         "that actually determine whether the wall stays dry. It also builds the wall out "
         "past the existing window and door trim, which rarely looks right.</p>"),
        ("Do you do soffit, fascia and eavestrough as well?",
         "<p>Yes, and it is worth doing at the same time. The soffit, fascia and trough all "
         "tie into the top course of siding, so doing them together gives one clean detail "
         "and one crew responsible for it. Splitting the work across two contractors is "
         "where the finger-pointing starts if water gets in at that junction.</p>"),
        ("What if you find rot once the old siding is off?",
         "<p>We photograph it, show you, and price the repair against the allowance we set "
         "in the original quote. We would rather build a realistic sheathing allowance into "
         "the number up front than come back to you mid-job with a surprise. On a house of "
         "1950s vintage some sheathing repair is likely, not exceptional.</p>"),
        ("Will new siding make my house warmer?",
         "<p>On its own, only slightly. What makes the difference is what goes on with it: "
         "continuous exterior insulation, a properly sealed weather barrier, and closing the "
         "air leaks that a tear-off exposes. If lower heating bills are the goal, say so at "
         "the quote stage and we will price the wall assembly rather than just the "
         "cladding.</p>"),
    ],
})

# --- Windows ----------------------------------------------------------------

_add({
    "slug": "windows",
    "nav": "Windows",
    "h1": "Window Replacement in Cornwall, Ontario",
    "title": "Window Replacement Cornwall, Ontario | Elite Carpentry",
    "desc": ("Window and door replacement in Cornwall, Akwesasne and SD&G. ENERGY STAR units "
             "air-sealed and properly flashed, including egress. Free quotes."),
    "eyebrow": "Windows &amp; doors",
    "service_type": "Window replacement",
    "lead": ("ENERGY STAR windows and doors, installed square, air-sealed and properly "
             "flashed &mdash; because a good window fitted badly performs like a bad window."),
    "intro": [
        ("Most of the performance you pay for in a new window is won or lost in the two "
         "hours it takes to install it. A high-spec triple-glazed unit stuffed into a rough "
         "opening with a bead of foam and no flashing will still be draughty, and it will "
         "still let water into the wall. The glass is the easy part."),
        ("We install square and plumb, shim at the load points rather than wherever is "
         "convenient, use low-expansion foam so the frame is not bowed by its own "
         "insulation, seal the interior air barrier, and flash the exterior so water that "
         "reaches the opening is directed back out. Then we finish the trim properly, inside "
         "and out, so the job is actually done."),
    ],
    "items_head": "What a window replacement includes",
    "items": [
        ("Measure and specification",
         "Every opening measured individually &mdash; older Cornwall homes are rarely square, "
         "and ordering from one measurement repeated across a house is how you end up with "
         "gaps stuffed with foam."),
        ("Retrofit or full-frame",
         "We will tell you honestly which one your house needs. Full-frame costs more and is "
         "the right answer when the existing frame is rotten or the wall needs to be sealed "
         "properly; retrofit is fine when the frame is sound."),
        ("Air sealing",
         "Low-expansion foam plus a sealed interior air barrier. This is where the comfort "
         "difference actually comes from, and it is the step most often skipped."),
        ("Exterior flashing and capping",
         "Sill pan and head flashing so water is shed outward, and aluminum capping on "
         "exterior trim for a finish that does not need painting."),
        ("Interior trim and finish",
         "Casing, sills and caulking finished to a paint-ready standard. We leave the room "
         "usable, not full of unfinished openings."),
        ("Basement egress windows",
         "Enlarging a basement opening to meet the Ontario Building Code egress requirement "
         "for a bedroom, including the cutting, lintel and window well. Needed for any "
         "legal basement bedroom."),
    ],
    "options_head": "Windows and doors we install",
    "options_intro": "Matched to the opening, the room and the exposure.",
    "options": [
        ("Casement and awning",
         "Crank-operated, and they seal against the frame under compression, which makes "
         "them the best performers against wind-driven rain and draughts. The default choice "
         "for exposed elevations.",
         ["Best air-tightness", "Full opening for ventilation", "Ideal for exposed walls"]),
        ("Double and single hung",
         "The traditional look for older Cornwall homes and heritage-style elevations. Slide "
         "vertically, so they take no exterior space over a walkway or patio.",
         ["Classic appearance", "No exterior swing", "Tilt-in cleaning options"]),
        ("Sliders and picture windows",
         "Sliders for wide openings, fixed picture units where the priority is light and "
         "view rather than ventilation. Fixed units are the most air-tight of all, because "
         "there is nothing to seal.",
         ["Maximum glass area", "Cost-effective on wide openings", "Fixed units seal best"]),
        ("Entry and patio doors",
         "Insulated steel and fibreglass entry doors, sliding and swing patio doors. Doors "
         "are where air leakage is most noticeable, so hardware quality and threshold detail "
         "matter more than the slab.",
         ["Insulated fibreglass and steel", "Multi-point locking available",
          "Sliding and swing patio"]),
    ],
    "callout": ("Ontario&rsquo;s Home Renovation Savings Program &mdash; $100 per opening",
                "<p>Ontario&rsquo;s Home Renovation Savings Program offers <strong>$100 per "
                "eligible ENERGY STAR-certified window or door rough opening</strong>, with the "
                "current funding window running to <strong>30&nbsp;November&nbsp;2026</strong>. "
                "Across a whole-house replacement that adds up.</p>"
                "<p>The rebate can only be claimed when the work is done by a contractor "
                "registered with the program as a Participating Contractor, and larger bundled "
                "rebates (combining windows with insulation and air sealing) require a pre- and "
                "post-retrofit energy assessment. Ask us where your project stands before you "
                "order, and confirm the current program terms at "
                "<a href=\"https://www.saveonenergy.ca/homerenovationsavings\" rel=\"noopener\">"
                "saveonenergy.ca</a> &mdash; terms and deadlines change.</p>"),
    "faqs": [
        ("Is there a rebate for replacing windows in Ontario?",
         "<p>Yes. Ontario's Home Renovation Savings Program pays $100 per eligible ENERGY "
         "STAR-certified window or door rough opening, with the current funding window "
         "running to 30 November 2026. It has to be claimed through a contractor registered "
         "with the program, and bundling windows with insulation and air sealing can unlock "
         "larger totals but requires an energy assessment before and after. Confirm the "
         "current terms on the Save on Energy website before budgeting around it.</p>"),
        ("How much does window replacement cost in Cornwall?",
         "<p>Published figures for standard vinyl replacement windows in this area have "
         "ranged from roughly $300 to $800 per window installed, but that spread is wide "
         "because it hides the variables that matter: window type, glazing package, whether "
         "the install is retrofit or full-frame, and whether the opening needs structural "
         "work. Casements cost more than sliders. Full-frame costs more than retrofit. We "
         "quote per opening, in writing.</p>"),
        ("Should I get double or triple glazing?",
         "<p>Triple glazing is meaningfully better in an Eastern Ontario winter, and the "
         "difference you actually notice is not the heating bill &mdash; it is that the glass "
         "is not cold to sit beside, and the condensation stops. It costs more and it is "
         "heavier. On a north-facing wall or a room you use every day, we would spend the "
         "money. On a rarely-used space, double glazing is fine.</p>"),
        ("What is the difference between retrofit and full-frame installation?",
         "<p>Retrofit leaves the existing frame in place and fits the new window into it. It "
         "is faster, cheaper and less disruptive, and it slightly reduces your glass area. "
         "Full-frame removes everything back to the rough opening, which is the only way to "
         "inspect for rot, install a proper sill pan and air-seal the opening correctly. If "
         "the existing frames are sound, retrofit is fine. If there is any rot or draught at "
         "the perimeter, full-frame is the honest answer.</p>"),
        ("Do I need a permit to add or enlarge a window?",
         "<p>Replacing a window in an existing opening generally does not need one. Cutting "
         "a new opening or enlarging an existing one does, because it affects the "
         "structure &mdash; a header or lintel has to carry the load above. Basement egress "
         "windows for a bedroom almost always fall into this category, and they have minimum "
         "size and opening requirements under the Ontario Building Code. We handle the "
         "permit application.</p>"),
    ],
})

# --- Bathrooms --------------------------------------------------------------

_add({
    "slug": "bathroom-renovations",
    "nav": "Bathrooms",
    "h1": "Bathroom Renovations in Cornwall, Ontario",
    "title": "Bathroom Renovations Cornwall, Ontario | Elite Carpentry",
    "desc": ("Bathroom renovation contractors in Cornwall, Akwesasne and SD&G. Full remodels, "
             "tub-to-shower conversions and walk-ins, properly waterproofed."),
    "eyebrow": "Bathroom renovations",
    "service_type": "Bathroom renovation",
    "lead": ("Full gut-and-rebuild bathrooms, tub-to-shower conversions and accessible "
             "walk-ins &mdash; waterproofed behind the tile, where it counts."),
    "intro": [
        ("A bathroom is the smallest room in the house and the most complicated thing in it. "
         "Plumbing, electrical, ventilation, waterproofing and finish carpentry all have to "
         "land within a few square metres, in the right order, and any one of them done "
         "poorly ruins the others."),
        ("The failure is almost always water, and almost always invisible for the first few "
         "years. Tile and grout are not waterproof &mdash; grout is porous, and the membrane "
         "behind the tile is what actually keeps water out of your floor joists. We install "
         "a proper waterproofing system on every wet area, we vent the fan to the outside "
         "rather than into the attic, and we coordinate the licensed trades so nothing gets "
         "closed up before it has been inspected."),
    ],
    "items_head": "What a bathroom renovation covers",
    "items": [
        ("Layout and design",
         "Working out what actually fits. Many Cornwall bathrooms in 1950s and 1960s houses "
         "are tight; moving a wall or relocating a door often buys more usable space than "
         "any fixture choice."),
        ("Demolition and disposal",
         "Full strip-out with the room contained and dust managed, and everything hauled "
         "away. We also look at what the demolition exposes &mdash; old cast iron drains, "
         "previous leaks, and knob-and-tube wiring all turn up in houses of this age."),
        ("Plumbing and electrical",
         "Coordinated with licensed trades. Rough-in inspected before anything is closed in, "
         "GFCI protection where the Code requires it, and a fan sized to the room and "
         "ducted to the outside."),
        ("Waterproofing",
         "A bonded waterproofing membrane on shower walls and floors, sloped bases, and "
         "properly sealed corners and penetrations. This is the part of the job you will "
         "never see and the part that determines whether it lasts."),
        ("Tile and finishes",
         "Floor and wall tile, niches, benches and curbless entries, set flat with consistent "
         "grout lines. Heated floors if you want them &mdash; worth considering in this "
         "climate on a tile floor."),
        ("Vanity, fixtures and trim",
         "Vanity, counter, mirror, lighting, glass and hardware installed and finished, with "
         "the trim carpentry done to the same standard as the rest of your house."),
    ],
    "options_head": "Common bathroom projects",
    "options_intro": "The four we are asked for most often.",
    "options": [
        ("Full gut and rebuild",
         "Everything out to the studs and rebuilt. The right approach when the layout does "
         "not work, when there is known water damage, or when the plumbing and wiring are "
         "original to a mid-century house.",
         ["Layout can change", "All hidden issues addressed", "Longest timeline"]),
        ("Tub-to-shower conversion",
         "Removing a rarely-used tub for a full-size shower. The most requested single "
         "change we do, and usually the best value per dollar in an older home.",
         ["Gains usable space", "Easier to step into", "Often no layout change needed"]),
        ("Accessible and walk-in",
         "Curbless entry, grab bar blocking built into the walls, wider door openings and "
         "bench seating. Worth building in now even if the need is years away &mdash; blocking "
         "costs almost nothing at framing stage and is a demolition job later.",
         ["Curbless and low-threshold entries", "Blocking for grab bars",
          "Slip-resistant flooring"]),
        ("Powder rooms and ensuites",
         "Small footprint, high impact. A powder room is often the fastest visible upgrade "
         "in a house, and an ensuite addition can usually be carved out of an oversized "
         "bedroom or closet.",
         ["Quick turnaround", "High visual impact", "Ensuite additions"]),
    ],
    "callout": ("What we find in older Cornwall bathrooms",
                "<p>Much of Cornwall&rsquo;s housing stock dates from the 1950s and 1960s, and "
                "on a full strip-out we regularly find the same three things: original cast "
                "iron drain stacks at the end of their life, no vapour barrier or ventilation "
                "behind the tile, and bathroom fans vented into the attic rather than through "
                "the roof.</p>"
                "<p>That last one quietly puts every shower&rsquo;s worth of moisture into your "
                "attic insulation all winter. None of these are unusual and none are "
                "catastrophic if they are found and dealt with while the walls are open. We "
                "quote a contingency for them rather than pretending a 70-year-old house will "
                "have no surprises.</p>"),
    "faqs": [
        ("How long does a bathroom renovation take?",
         "<p>For a full gut and rebuild, plan on two to four weeks of site time for a "
         "typical main bathroom, longer if the layout changes or if we find something behind "
         "the walls. The schedule is driven less by our labour than by sequencing: rough-in "
         "inspection, waterproofing cure times, tile set and grout, then finishes. Rushing "
         "any of those is how a bathroom fails early. We give you a written schedule before "
         "we start.</p>"),
        ("Can I use the bathroom during the renovation?",
         "<p>Not the one being renovated. If it is your only bathroom, that is the single "
         "most important thing to plan around, and we will sequence the work to minimise the "
         "days without a working toilet rather than treating it as your problem. Tell us at "
         "the quote stage if it is your only bathroom &mdash; it genuinely changes how we plan "
         "the job.</p>"),
        ("Do I need a permit for a bathroom renovation?",
         "<p>Replacing fixtures in the same locations generally does not require one. Moving "
         "plumbing, altering structure, or adding a new bathroom does. Anything that changes "
         "drainage or venting is plumbing permit territory. We confirm with the City's "
         "Building Division for your specific scope and handle the application where one is "
         "needed.</p>"),
        ("Is tile waterproof on its own?",
         "<p>No, and this is the most costly misunderstanding in bathroom renovation. Grout "
         "is porous and tile assemblies are not watertight. What keeps water out of your "
         "floor structure is the waterproofing membrane bonded behind and beneath the tile. "
         "A shower built without one will look identical on day one and will be rotting the "
         "subfloor by year five.</p>"),
        ("What does a bathroom renovation cost in Cornwall?",
         "<p>The variables that move the number most are whether the layout changes, whether "
         "plumbing has to be relocated, the size of the tiled area, and the fixture and tile "
         "selections &mdash; which can vary by several times over for the same footprint. A "
         "tub-to-shower conversion in an existing footprint sits at the low end; a full gut "
         "with a moved wall and a curbless shower at the high end. We quote itemised so you "
         "can see which choices are driving the cost and adjust them.</p>"),
    ],
})

# --- Kitchens ---------------------------------------------------------------

_add({
    "slug": "kitchen-renovations",
    "nav": "Kitchens",
    "h1": "Kitchen Renovations in Cornwall, Ontario",
    "title": "Kitchen Renovations Cornwall, Ontario | Elite Carpentry",
    "desc": ("Kitchen renovation contractors in Cornwall, Akwesasne and SD&G. Layout changes, "
             "custom cabinetry, islands and finish carpentry by one crew."),
    "eyebrow": "Kitchen renovations",
    "service_type": "Kitchen renovation",
    "lead": ("Layout changes, custom cabinetry, islands and finish carpentry &mdash; planned "
             "properly and run by one crew from demolition to the last piece of trim."),
    "intro": [
        ("A kitchen renovation is mostly a scheduling problem wearing a carpentry costume. "
         "Cabinets have lead times. Counters cannot be templated until the boxes are set. "
         "Electrical and plumbing have to be roughed in and inspected before drywall. Get "
         "the order wrong and a six-week job becomes a four-month one with a household "
         "washing dishes in the bathtub."),
        ("We plan the sequence before we swing a hammer, order the long-lead items first, "
         "and run the whole job with one crew and one point of contact. If a wall is coming "
         "out we establish early whether it is load-bearing, because removing one that is "
         "means a beam, a permit, and usually an engineer's drawing &mdash; and that is a "
         "conversation to have at the planning stage, not the demolition stage."),
    ],
    "items_head": "What a kitchen renovation covers",
    "items": [
        ("Layout planning",
         "Working through what the room can actually support &mdash; where services already "
         "run, what a wall removal would cost, and whether an island fits with the clearances "
         "you need to open a dishwasher."),
        ("Structural changes",
         "Opening a wall between the kitchen and living space, with the beam sized and the "
         "permit obtained. We establish load-bearing status early rather than finding out "
         "on demolition day."),
        ("Cabinetry",
         "Stock, semi-custom or fully custom built to the room. Custom earns its cost in "
         "older houses where the walls are not square and the ceilings are not level &mdash; "
         "which is most of the houses we work in."),
        ("Counters and backsplash",
         "Templated after the boxes are set so the fit is right, then tile or slab "
         "backsplash finished into the cabinetry and around outlets cleanly."),
        ("Electrical and plumbing",
         "Coordinated with licensed trades &mdash; circuits for modern appliance loads, counter "
         "receptacles to Code, under-cabinet lighting, and sink and dishwasher relocations."),
        ("Flooring and finish carpentry",
         "Flooring, trim, crown, panelling and toe kicks. The finish carpentry is what makes "
         "a kitchen look built-in rather than installed, and it is the part we care most "
         "about."),
    ],
    "options_head": "Cabinetry, and where the money goes",
    "options_intro": ("Cabinets are usually the largest line on a kitchen quote, so it is "
                      "worth understanding the tiers."),
    "options": [
        ("Stock cabinetry",
         "Pre-made in fixed sizes. The fastest and least expensive route, and perfectly good "
         "when the layout is straightforward. The compromise is filler panels wherever your "
         "wall dimensions do not match the increments available.",
         ["Shortest lead time", "Lowest cost", "Fixed sizes mean filler panels"]),
        ("Semi-custom",
         "Stock construction with real choice in sizes, finishes and internal fittings. For "
         "most kitchens this is the sensible middle, and it is where we point people who "
         "want a specific look without a fully bespoke budget.",
         ["Wide finish and size range", "Better internal hardware", "Moderate lead time"]),
        ("Full custom",
         "Built to your room's actual dimensions. Worth it when the house is old and nothing "
         "is square, when ceiling height should be used properly, or when you want something "
         "no catalogue offers &mdash; an integrated appliance run, an unusual island, a "
         "built-in banquette.",
         ["Built to the room", "Uses every inch of height", "Longest lead time"]),
    ],
    "callout": ("Before you plan on removing that wall",
                "<p>Opening up a kitchen into a living or dining room is the most requested "
                "change we get, and it is very often the right one. But whether the wall is "
                "load-bearing changes the job substantially: a structural wall needs a properly "
                "sized beam, posts carrying down to adequate support, a building permit, and in "
                "most cases an engineer&rsquo;s drawing.</p>"
                "<p>None of that is a reason not to do it. It is a reason to know before you "
                "budget, rather than three days into demolition. We assess it during "
                "quoting &mdash; and we would rather tell you it is a bigger job than you hoped "
                "than discover it with your kitchen already in a skip.</p>"),
    "faqs": [
        ("How long does a kitchen renovation take?",
         "<p>Six to twelve weeks on site is typical for a full kitchen, but the critical "
         "path usually starts well before that: cabinetry lead times commonly run several "
         "weeks from the date the order is finalised, and counters cannot be templated until "
         "the cabinets are physically installed. We order long-lead items first and give you "
         "a written schedule, so the time without a kitchen is as short and as predictable as "
         "we can make it.</p>"),
        ("Do I need a permit for a kitchen renovation?",
         "<p>Replacing cabinets, counters and finishes in the existing layout generally does "
         "not. Removing or altering a load-bearing wall does, and so does moving plumbing or "
         "adding new circuits in most cases. If a permit is required we prepare and file the "
         "application, and we arrange the engineer's drawing when a beam calculation is "
         "needed.</p>"),
        ("Can I stay in the house during the work?",
         "<p>Almost always, yes &mdash; the kitchen is out of use, not the house. What helps "
         "most is setting up a temporary kitchen somewhere else before demolition: fridge, "
         "microwave, kettle and a sink you can reach. We will tell you which weeks will be "
         "the loudest and dustiest so you can plan around them.</p>"),
        ("Should I get custom or stock cabinets?",
         "<p>It depends on the house more than the budget. In a newer home with square walls "
         "and standard ceilings, stock or semi-custom cabinetry fits well and the money is "
         "better spent on counters and appliances. In an older Cornwall home where nothing "
         "is plumb and the ceilings are an unusual height, custom stops looking like a "
         "luxury and starts looking like the only way to avoid a row of filler strips.</p>"),
        ("Do you handle the plumbing and electrical too?",
         "<p>We coordinate them. The plumbing and electrical work is carried out by licensed "
         "trades, scheduled and managed by us as part of the job, and inspected before "
         "anything is closed in. You get one point of contact and one schedule rather than "
         "having to chase three contractors yourself.</p>"),
    ],
})
