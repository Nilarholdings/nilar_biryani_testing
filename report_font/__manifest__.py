# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Font",
    "version": "0.1",
    "author": "Nilar Holdings",
    "website": "https://www.nilarholdings.com",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Base module for mm font rendering in qweb report",
    'images': ['report_font/static/description/fonts.png'],
    "depends": [
        "base",
        "web",
    ],
    "data": [
    ],
    'assets': {
        'web.assets_frontend': [
            'report_font/static/src/scss/fonts.scss',
        ],
        'web.assets_qweb': [
            'report_font/static/src/scss/fonts.scss',
        ],
        'web.report_assets_common': [
            'report_font/static/src/scss/fonts.scss',
        ],
    },
}
