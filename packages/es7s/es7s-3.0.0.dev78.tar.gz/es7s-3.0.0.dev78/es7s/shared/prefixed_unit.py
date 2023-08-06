# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import io
import re

import pytermor as pt



class DemoText:
    DATA = (
        "te 0 xt 1 tetext tee 12 k text t 44pm text t 1s text text text text text tee 1 second text text text text "
        "texe extt 2 text text tee 16K text text texte 400pA texte 5sec text text text text te 5 secs text text "
        "text texe te textet 3% tex 0.00 text 21Mb text t 125nm texte 4m 22s text text text texte 4min 22sec text "
        "text text text tee  ext 40% text text texte 25.54 M text te 5nV text text texte 12min text text text text "
        "t 12 minutes text te tex extt 12.03% texe 33gb text t 60μs texte 6h text text text text text tee 4 hour "
        "text text text text text tee te tet 5k text text te 37G text text texte 300ms texte 12h 23m text text "
        "text text tee 12 hr 23 min text texe te  xt 6.6k text t 41.1GHz text te 11kHz texte 2 d 12 hr text text "
        "tee 2 days 12h text text text text text te text extet 72.1K texte 466GB texte 0.166K text tee 5wk text "
        "text text text tee 5 weeks text text text text text tex tt 801M text t 0.51T texte 0.233M text tee 1mo "
        "text text text text tee 1 month text text text text text tex te textt 9000ms texe 0.77Tb texe 0.345G text "
        "tee 6mon 12d text t 6 months 12 days text text text text text texe t xtet 10K text text texte 1PB text "
        "text texte 0.666T text tee 1y 4mo text text te 1 year 4 months text texte te extt 12 kb/s text te 10Pbit "
        "texe 0.981P text tee 31yr 6mon texte 31 year 6 months text text text text text tex"
    )

    @classmethod
    def make_io(cls) -> io.StringIO:
        return io.StringIO(cls.DATA)
