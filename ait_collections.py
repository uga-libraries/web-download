# Archive-it (AIT) collection title and identifiers.
# This is a separate file to make it faster to find and update.

# The AIT collection you download the most PDFs from.
# The menu in the GUI will start with this selected.
# Use ait_coll_default = "" if you don't want anything to be pre-selected.
ait_coll_default = "Georgia Government Publications"

# All AIT collections you download PDFs from.
# It is used to populate the menu in the GUI, verify there were no errors when providing the collection to the script,
# and to translate the collection name (easier for users) to the collection ID needed to construct the URLs.
# The information is formatted "AIT Title": "AIT ID".
# Get this information from the public or staff AIT interfaces. The ID is the part of the URL after /collections/.
ait_coll_dict = {"Activists and Advocates": "12263",
                 "Business": "12939",
                 "Georgia Disability History Archive": "12264",
                 "Georgia Government Publications": "15678",
                 "Georgia Politics": "12265",
                 "Legal": "12944",
                 "Political Observers": "12262",
                 "University of Georgia Academics": "16951",
                 "University of Georgia Administration": "12912",
                 "University of Georgia Athletics": "12907",
                 "University of Georgia Student Life": "12181"}
