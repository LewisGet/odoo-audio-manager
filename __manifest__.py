{
    "name": "lj audio manager",
    "version": "1.0",
    "author": "Lewis Jang",
    "depends": ["base"],
    "external_dependencies": {
        "python": ['pydub']
    },
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/audio_views.xml"
    ],
    "installable": True,
    "application": True,
}
