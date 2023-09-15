{
    "name": "estate",
    "version": "0.0.1",
    "summary": "Real State Advertisments",
    "description": """
        Manage Sales of your properties
    """,
    "author": "Sualasoft SARL",
    "website": "https://sualasoft.com",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
