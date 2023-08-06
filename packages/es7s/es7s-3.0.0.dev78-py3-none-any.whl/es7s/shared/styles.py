# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import pytermor as pt


class Styles(pt.Styles):
    TEXT_DISABLED = pt.Style(fg=pt.cv.GRAY_23)
    TEXT_LABEL = pt.Style(fg=pt.cv.GRAY_35)
    TEXT_AUXILIARY = pt.Style(fg=pt.cv.GRAY_50)
    TEXT_UNITS = TEXT_AUXILIARY
    TEXT_DEFAULT = pt.Style(fg=pt.cv.GRAY_62)
    TEXT_MAIN_VALUE = pt.Style(TEXT_DEFAULT, bold=True)
    TEXT_ACCENT = pt.Style(fg=pt.cv.GRAY_85)
    TEXT_SUBTITLE = pt.Style(fg=pt.cv.GRAY_93, bold=True)
    TEXT_TITLE = pt.Style(fg=pt.cv.HI_WHITE, bold=True, underlined=True)

    BORDER_DEFAULT = pt.Style(fg=pt.cv.GRAY_30)
    FILL_DEFAULT = pt.Style(fg=pt.cv.GRAY_46)

    STDERR_DEBUG = pt.Style(fg=pt.Color256.get_by_code(60))
    STDERR_TRACE = pt.Style(fg=pt.Color256.get_by_code(66))
