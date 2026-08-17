#!/usr/bin/env python3
"""
Per-location page content.

Each page is written from scratch. Six pages with a town name swapped in is
thin content, and Google has been discounting it for years. What makes these
pages genuinely different is that the towns genuinely are: they sit in five
different municipalities with five different building departments, and their
housing stock has different ages and different failure modes.

FACT-CHECK BEFORE LAUNCH. Sources for the figures used below:
  - Cornwall pop. 47,845 (2021 Census); seat of SD&G; Building Division (613) 930-2787
  - South Glengarry pop. 13,330 (2021); ~45 km of Lake St. Francis shoreline
  - North Glengarry pop. 10,144 (2021); Alexandria pop. 3,287; Building & Planning (613) 525-1116
  - Long Sault and Ingleside built 1957-58 to rehouse the Lost Villages flooded
    by the St. Lawrence Seaway; both in the Township of South Stormont
  - Akwesasne: Kawehno:ke (Cornwall Island) is the Ontario portion, under the
    Mohawk Council of Akwesasne, not the City of Cornwall

*** OPEN QUESTION FOR THE OWNER: does he work the New York (Saint Regis Mohawk
Tribe) portion of Akwesasne as well? This page is scoped to the Ontario/MCA
portion only. Cross-border work has customs, licensing and insurance
implications that must not be implied until confirmed. ***
"""

LOCATIONS = {}


def _add(d):
    LOCATIONS[d["slug"]] = d


_add({
    "slug": "cornwall",
    "name": "Cornwall",
    "region": "City of Cornwall",
    "h1": "Carpentry &amp; Renovation Contractors in Cornwall, Ontario",
    "title": "Renovation Contractors in Cornwall, ON | Elite Carpentry",
    "desc": ("Local carpentry and renovation contractors in Cornwall, Ontario. Decks, fences, "
             "siding, windows, bathrooms and kitchens, with City permits handled."),
    "lead": ("Our home base. Decks, fences, siding, windows, bathrooms and kitchens across "
             "Cornwall &mdash; from Riverdale to the east end, with the City permit paperwork "
             "handled for you."),
    "intro": [
        ("Cornwall is where we are based and where we do most of our work. It is the seat of "
         "the United Counties of Stormont, Dundas and Glengarry and, at roughly 47,800 "
         "people, the largest centre between Ottawa and Montreal on this stretch of the "
         "St.&nbsp;Lawrence."),
        ("For a renovation crew, what matters about Cornwall is the housing stock. A large "
         "share of the city was built in the post-war decades and again through the Seaway "
         "years, which means an enormous number of houses are now hitting the age where the "
         "original siding, windows, wiring and bathrooms all come due at once. We spend most "
         "of our year on exactly that work."),
    ],
    "notes": [
        ("Post-war housing, all ageing at once",
         "Cornwall's 1950s and 1960s bungalows share a set of predictable issues: original "
         "cladding with no weather barrier behind it, bathroom fans vented into the attic, "
         "undersized electrical, and cast iron drains at the end of their life. We know what "
         "to look for and we price a realistic contingency instead of pretending a "
         "70-year-old house will have no surprises."),
        ("Permits go through the City's Building Division",
         "Cornwall is its own municipality with its own Building Division, reachable at "
         "(613)&nbsp;930-2787. Decks more than 60&nbsp;cm above grade need a permit; so do "
         "structural changes, new window openings and most plumbing relocations. We prepare "
         "the drawings and file the application as part of the job."),
        ("Weather off the river",
         "Exposure along the St.&nbsp;Lawrence is harder on south-facing walls, windows and "
         "decks than it is a few kilometres inland. Wind-driven rain finds any flashing "
         "detail that was skipped. It is a reason we specify casement windows on exposed "
         "elevations and why we are unreasonably particular about kick-out flashing."),
    ],
    "areas": ["Riverdale", "Le Village", "Eastcourt", "Cornwall Centre", "Sunrise",
              "Cotton Mills district", "Guindon Park area", "Northend"],
    "nearby": ["Akwesasne", "Long Sault", "Glen Walter", "St. Andrew's West",
               "Bonville", "Summerstown"],
    "faqs": [
        ("Do you charge for quotes in Cornwall?",
         "<p>No. Quotes are free, in writing and itemised, so you can see what is driving "
         "the number and adjust the scope if you want to. We are based in Cornwall, so there "
         "is no travel charge built into a city quote either.</p>"),
        ("Do you handle the building permit?",
         "<p>Yes. Where the work needs a permit we prepare the drawings and file the "
         "application with the City of Cornwall Building Division, and we meet the inspector "
         "on site. You do not need to take a day off work for it.</p>"),
        ("How quickly can you start?",
         "<p>It depends on the season and the trade. Exterior work &mdash; decks, fencing, "
         "siding &mdash; books up through spring and summer, so the earlier you ask the better. "
         "Interior work like bathrooms and kitchens is easier to schedule through the winter, "
         "and winter is genuinely a good time to do it. We will give you a realistic date "
         "rather than an optimistic one.</p>"),
    ],
})

_add({
    "slug": "akwesasne",
    "name": "Akwesasne",
    "region": "Mohawk Territory of Akwesasne",
    "h1": "Carpentry &amp; Renovation Services in Akwesasne",
    "title": "Carpentry &amp; Renovations in Akwesasne | Elite Carpentry",
    "desc": ("Carpentry and renovation services for Akwesasne, including Kawehno:ke. Decks, "
             "fencing, siding, windows, bathrooms and kitchens. Free quotes."),
    "lead": ("Decks, fencing, siding, windows and full interior renovations across the "
             "Ontario portion of Akwesasne, including Kawehno:ke."),
    "intro": [
        ("Akwesasne is immediately south of us across the river, and it is a community we "
         "work in regularly. Kawehno:ke &mdash; Cornwall Island &mdash; is the Ontario portion "
         "of the territory, and travel between Cornwall and Kawehno:ke is domestic, so "
         "getting a crew and materials on site is straightforward."),
        ("What is not the same as a Cornwall job is the administration. Akwesasne is not "
         "under the City of Cornwall. The northern portion of the territory falls under the "
         "Mohawk Council of Akwesasne, which has its own processes for construction and "
         "property matters. We work to whatever the Council's requirements are for your "
         "project rather than assuming the City's process applies, and we ask that question "
         "at the quote stage instead of finding out later."),
    ],
    "notes": [
        ("Local jurisdiction, not City of Cornwall",
         "Permitting, approvals and property requirements in the Ontario portion of "
         "Akwesasne run through the Mohawk Council of Akwesasne, not the City. We confirm "
         "the applicable process with the Council for your specific project before we start, "
         "and we build the time for it into the schedule."),
        ("Riverfront exposure",
         "A lot of the territory sits directly on the water. Riverfront properties get more "
         "wind, more driven rain and more ice than sheltered inland lots, which changes what "
         "we would specify &mdash; heavier deck framing and railings, casement windows over "
         "sliders on exposed walls, and particular attention to how the cladding is fastened."),
        ("Same crew, same standard",
         "This is not a satellite operation. The people who quote your job are the people "
         "who build it, working to the Ontario Building Code and to the same standard we "
         "hold on a Cornwall job."),
    ],
    "areas": ["Kawehno:ke (Cornwall Island)", "Riverfront properties", "Year-round homes",
              "Seasonal and camp properties"],
    "nearby": ["Cornwall", "Glen Walter", "Summerstown", "South Stormont"],
    "faqs": [
        ("Do you work in Akwesasne?",
         "<p>Yes. We regularly work in the Ontario portion of the territory, including "
         "Kawehno:ke (Cornwall Island). Travel between Cornwall and Kawehno:ke is domestic, "
         "so scheduling a crew and delivering materials is no different from any other local "
         "job.</p>"),
        ("How does permitting work for a project in Akwesasne?",
         "<p>Differently from Cornwall. The northern portion of Akwesasne falls under the "
         "Mohawk Council of Akwesasne rather than the City, and the Council has its own "
         "requirements for construction and property matters. We confirm what applies to "
         "your specific project with the Council before quoting, and we allow for it in the "
         "schedule rather than treating it as an afterthought.</p>"),
        ("Is there a travel charge?",
         "<p>No. Akwesasne is one of our two core service areas, not an outlying one. Our "
         "quotes for the territory are priced the same way as our Cornwall quotes.</p>"),
    ],
})

_add({
    "slug": "long-sault",
    "name": "Long Sault",
    "region": "Township of South Stormont",
    "h1": "Carpentry &amp; Renovation Contractors in Long Sault, Ontario",
    "title": "Renovation Contractors in Long Sault, ON | Elite Carpentry",
    "desc": ("Carpentry and renovation contractors in Long Sault, Ontario. Decks, siding, "
             "windows, fencing and interior renovations for Seaway-era homes."),
    "lead": ("Ten minutes west of Cornwall, and a village where almost every original house "
             "went up in the same two years &mdash; which tells us a great deal before we even "
             "arrive."),
    "intro": [
        ("Long Sault is unusual, and the reason matters for renovation work. The village was "
         "purpose-built in 1957 and 1958 to rehouse families displaced when the "
         "St.&nbsp;Lawrence Seaway flooded the Lost Villages. It did not grow gradually the "
         "way most towns do &mdash; a large share of it was constructed at once, to the "
         "standards of that moment."),
        ("Which means the original housing stock is now approaching seventy years old, more "
         "or less all at the same time. Siding, windows, roofs, bathrooms and wiring across "
         "the village are reaching end of life on roughly the same schedule. We do a lot of "
         "work here, and we usually have a fair idea of what is behind the wall before we "
         "open it."),
    ],
    "notes": [
        ("A village built in two years",
         "The original 1957&ndash;58 houses share construction details, which makes them "
         "predictable to work on. What we typically find on a re-side is no weather barrier "
         "behind the cladding and no head flashing over the window openings &mdash; normal for "
         "the period, and the one chance to correct it is when the old siding comes off."),
        ("Permits go through South Stormont",
         "Long Sault is in the Township of South Stormont, not the City of Cornwall, so "
         "permits and zoning go through the Township's building department. Different office, "
         "different fee schedule, sometimes different setback rules. We confirm the "
         "requirements with the Township rather than assuming Cornwall's apply."),
        ("Mature lots and established trees",
         "Seventy years on, these are properties with big trees, settled grades and often an "
         "older deck or fence already in place. That affects access for equipment, where "
         "footings can realistically go, and whether an existing structure is worth "
         "resurfacing or should come out entirely."),
    ],
    "areas": ["Original 1957&ndash;58 village", "Ault Park area", "Long Sault Parkway side",
              "Newer subdivisions"],
    "nearby": ["Ingleside", "Cornwall", "Moulinette", "Milles Roches", "Newington"],
    "faqs": [
        ("Do you travel to Long Sault?",
         "<p>Regularly. It is about ten minutes from our base in Cornwall and one of the "
         "areas we work in most often, largely because of the age of the original village "
         "housing. There is no travel surcharge.</p>"),
        ("Who issues building permits in Long Sault?",
         "<p>The Township of South Stormont, not the City of Cornwall. The fee schedule and "
         "some zoning provisions differ from Cornwall's, so we confirm the current "
         "requirements with the Township before quoting and we file the application on your "
         "behalf.</p>"),
        ("My house is one of the original 1950s builds. What should I expect?",
         "<p>Expect the hidden work to be a real part of the job. On houses of that vintage "
         "we routinely find no house wrap behind the siding, missing flashing over windows, "
         "some sheathing repair, and bathroom fans ducted into the attic instead of through "
         "the roof. None of it is unusual and none of it is a disaster &mdash; but a quote that "
         "does not allow for any of it is a quote that will change once work starts. Ours "
         "includes an allowance and tells you what it is.</p>"),
    ],
})

_add({
    "slug": "ingleside",
    "name": "Ingleside",
    "region": "Township of South Stormont",
    "h1": "Carpentry &amp; Renovation Contractors in Ingleside, Ontario",
    "title": "Renovation Contractors in Ingleside, ON | Elite Carpentry",
    "desc": ("Carpentry and renovation contractors in Ingleside, Ontario. Siding, windows, "
             "decks, fencing, bathrooms and kitchens for Seaway-era homes."),
    "lead": ("Ingleside shares Long Sault&rsquo;s history and its housing stock &mdash; a "
             "planned village from 1957&ndash;58, now all reaching the same renovation "
             "milestones together."),
    "intro": [
        ("Like its neighbour to the east, Ingleside was created to rehouse families displaced "
         "by the flooding of the Lost Villages when the St.&nbsp;Lawrence Seaway was built. "
         "It is a planned community, laid out and constructed in 1957 and 1958, and it has a "
         "settled, green, deliberately-designed feel that newer subdivisions rarely achieve."),
        ("From a building perspective it means the same thing as Long Sault: a concentrated "
         "stock of houses that are all around seventy years old. The work we are asked for "
         "here is heavily weighted towards the envelope &mdash; siding, soffit, fascia, "
         "eavestrough and windows &mdash; because that is what wears out first and what makes "
         "the biggest difference to comfort and heating cost."),
    ],
    "notes": [
        ("Envelope work is most of what we do here",
         "Re-siding a Seaway-era house is the moment to add the things it never had: a "
         "proper weather barrier, head flashing over every window, kick-out flashing where "
         "roofs meet walls, and correctly vented soffit. Done together with a window "
         "replacement it is a genuine step change in how the house feels in January."),
        ("South Stormont handles the permits",
         "Ingleside is in the Township of South Stormont. Permits, zoning and setbacks go "
         "through the Township office rather than the City of Cornwall, and we confirm the "
         "current requirements there before quoting any work that needs one."),
        ("Rebate stacking is worth a conversation",
         "On a house of this age, windows are rarely the only thing that would benefit. "
         "Ontario's Home Renovation Savings Program pays per eligible ENERGY STAR opening "
         "and offers larger amounts for bundled work &mdash; insulation, air sealing and "
         "windows together &mdash; though bundling requires an energy assessment. Worth "
         "understanding before you commit to a scope."),
    ],
    "areas": ["Original planned village", "Farran Park area", "Waterfront properties",
              "Newer builds"],
    "nearby": ["Long Sault", "Cornwall", "Newington", "Osnabruck Centre", "Morrisburg"],
    "faqs": [
        ("Do you serve Ingleside?",
         "<p>Yes, regularly. It is about twenty minutes west of Cornwall and, together with "
         "Long Sault, one of the areas where we do the most envelope work &mdash; siding, "
         "soffit, fascia and windows &mdash; because of the age of the original village "
         "housing.</p>"),
        ("Should I do siding and windows at the same time?",
         "<p>If both are due, yes, and it is not a sales answer. The window flashing and the "
         "weather barrier are the same detail, and doing them together is the only way to "
         "integrate them properly. Split across two jobs and two contractors, that junction "
         "is exactly where water gets in and where nobody accepts responsibility.</p>"),
        ("Who do I get a permit from in Ingleside?",
         "<p>The Township of South Stormont. Cornwall's Building Division does not cover "
         "Ingleside, so the fee schedule and some zoning provisions differ. We confirm what "
         "applies and file the application for you.</p>"),
    ],
})

_add({
    "slug": "lancaster-glen-walter",
    "name": "Lancaster &amp; Glen Walter",
    "region": "Township of South Glengarry",
    "h1": "Carpentry &amp; Renovation Contractors in Lancaster &amp; Glen Walter",
    "title": "Renovations in Lancaster &amp; Glen Walter | Elite Carpentry",
    "desc": ("Renovation contractors serving Lancaster, South Lancaster and Glen Walter. "
             "Waterfront decks, siding, windows and interior renovations."),
    "lead": ("East of Cornwall along the Lake St.&nbsp;Francis shoreline &mdash; waterfront "
             "decks, exposed elevations, and a lot of properties where the view is the whole "
             "point."),
    "intro": [
        ("Glen Walter sits immediately east of Cornwall and Lancaster a little further along, "
         "both in the Township of South Glengarry. The township runs roughly 45 kilometres of "
         "Lake St.&nbsp;Francis shoreline &mdash; the widening of the St.&nbsp;Lawrence east of "
         "the city &mdash; and a large share of the work we do out here is waterfront."),
        ("Waterfront changes the build. Wind and driven rain hit these houses harder than an "
         "inland lot, ice does more damage, and the whole reason for the deck is usually the "
         "view, which pushes you towards glass or cable railing rather than pickets. It also "
         "means shoreline setbacks and conservation authority rules can apply on top of the "
         "township's own zoning, so what you can build and where is worth establishing before "
         "you get attached to a design."),
    ],
    "notes": [
        ("Built for the view",
         "On a waterfront lot the railing choice matters more than anywhere else. Glass "
         "panels and cable systems keep the sightline that you bought the property for, and "
         "both meet Code when specified properly. We will show you what each looks like from "
         "inside the house, not just from the yard."),
        ("Exposure drives the specification",
         "More wind and more driven rain means heavier framing, closer fastener spacing, and "
         "casement windows over sliders on the water-facing elevation. We would rather "
         "over-build the connections on an exposed lot than come back in five years."),
        ("South Glengarry permits, and possibly more",
         "Permits go through the Township of South Glengarry. On shoreline properties there "
         "may also be conservation authority requirements and shoreline setbacks on top of "
         "the township zoning. We establish what applies before quoting rather than "
         "discovering it at the application stage."),
    ],
    "areas": ["Glen Walter", "Lancaster", "South Lancaster", "Waterfront properties",
              "Williamstown", "Martintown"],
    "nearby": ["Cornwall", "Summerstown", "Bainsville", "Williamstown", "Martintown"],
    "faqs": [
        ("Do you build waterfront decks on Lake St. Francis?",
         "<p>Yes, and it is a good share of our summer work. What differs from an inland "
         "deck is the exposure &mdash; more wind and driven rain, more ice &mdash; so we specify "
         "heavier connections and we pay closer attention to fastener spacing. Railing choice "
         "also matters more, because the point of the deck is usually the view.</p>"),
        ("Are there extra rules for building near the shoreline?",
         "<p>Often, yes. On top of the Township of South Glengarry's zoning there can be "
         "shoreline setbacks and conservation authority requirements affecting what you can "
         "build and how close to the water. It is the first thing we check on a waterfront "
         "property, because it determines the design rather than just the paperwork.</p>"),
        ("Do you cover Williamstown and Martintown too?",
         "<p>Yes. Both are in South Glengarry and both are comfortably within our normal "
         "working area, as are Summerstown and Bainsville. If you are anywhere in the "
         "township, ask.</p>"),
    ],
})

_add({
    "slug": "alexandria",
    "name": "Alexandria",
    "region": "Township of North Glengarry",
    "h1": "Carpentry &amp; Renovation Contractors in Alexandria, Ontario",
    "title": "Renovation Contractors in Alexandria, ON | Elite Carpentry",
    "desc": ("Renovation contractors serving Alexandria and North Glengarry. Decks, fencing, "
             "siding, windows, bathrooms and kitchens for village and rural homes."),
    "lead": ("North into Glengarry &mdash; village homes, farm properties and rural lots, where "
             "the constraints are well water, septic beds and older buildings worth keeping."),
    "intro": [
        ("Alexandria is the largest community in the Township of North Glengarry and the "
         "township's administrative seat, with a population of roughly 3,300 in a township of "
         "about 10,100. It is a different kind of work from Cornwall: more rural properties, "
         "more acreage, more older village housing, and a lot of buildings that are worth "
         "restoring rather than replacing."),
        ("Rural changes the practical constraints more than the carpentry. Septic beds "
         "determine where a deck or an addition can physically go. Well locations affect "
         "excavation. Longer driveways and softer ground affect when heavy material can be "
         "delivered. We plan around all of it up front, because on a rural lot the surprise "
         "is rarely the building &mdash; it is the site."),
    ],
    "notes": [
        ("Septic and well come first",
         "On a rural property the first question is not what you want to build but where it "
         "can go. Building over a septic bed or too close to a well is a problem that no "
         "amount of good carpentry fixes afterwards. We locate both before we design "
         "anything."),
        ("North Glengarry handles permits",
         "Alexandria is in the Township of North Glengarry, whose Building, Planning and "
         "By-law Enforcement department administers the Ontario Building Code locally. "
         "Different office and different fee schedule from Cornwall, and rural zoning "
         "provisions differ too. We confirm before quoting."),
        ("Older buildings worth keeping",
         "There is a lot of housing up here with genuine character and solid bones. Where a "
         "building is worth restoring we would rather restore it &mdash; matching existing "
         "trim profiles, repairing rather than replacing what is sound. It is more careful "
         "work and it is usually the better outcome."),
    ],
    "areas": ["Alexandria village", "Mill Pond area", "Rural and farm properties",
              "Maxville", "Glen Robertson", "Dunvegan"],
    "nearby": ["Maxville", "Green Valley", "Glen Robertson", "Apple Hill", "Cornwall"],
    "faqs": [
        ("Is Alexandria too far for you?",
         "<p>No. It is around forty minutes north of Cornwall and well within our normal "
         "working area, along with Maxville, Green Valley and the surrounding rural "
         "properties. For larger projects it makes no practical difference to how we "
         "schedule the work.</p>"),
        ("Can you build a deck or addition on a rural property with a septic system?",
         "<p>Usually, but the septic bed determines where. Building over a bed or its "
         "required clearance is not permitted and can wreck an expensive system. We locate "
         "the bed and the well before designing anything, and where the ideal spot is not "
         "available we will show you the alternatives before you set your heart on a "
         "layout.</p>"),
        ("Who issues building permits in Alexandria?",
         "<p>The Township of North Glengarry, through its Building, Planning and By-law "
         "Enforcement department. Different office, fee schedule and zoning provisions from "
         "the City of Cornwall &mdash; particularly for rural and agricultural properties. We "
         "confirm what applies and file on your behalf.</p>"),
    ],
})
