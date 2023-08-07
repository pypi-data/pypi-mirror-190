# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubic_bezier_spline']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'paragraphs>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'cubic-bezier-spline',
    'version': '0.3.1',
    'description': 'Create C2-continuous, non-rational cubic Bézier splines. In other words, this will approximate or interpolate a sequence of points into a sequence of non-rational cubic Bézier curves.',
    'long_description': '## Non-rational Bezier curves and splines (composite Bezier curves)\n\nThis package exists mostly to create C2-continuous, non-rational cubic Bezier splines. In other words, this will approximate or interpolate a sequence of points into a sequence of non-rational cubic Bezier curves.\n\nShould be relatively fast, but this isn\'t suited for heavy math. This is for taking some points you have and making a nice-looking curve out of them. Specifically, a cubic Bezier spline, which is made from the type of curves used in SVG, fonts, and other vector-base programs. I am only interested in feature requests that directly apply to that purpose. This is not an exercise in completism.\n\n### install\n\n    pip install cubic_bezier_spline\n\n### this package will\n\n* Evaluate, differentiate, elevate, and split non-rational Bezier curves of any degree\n* Construct non-rational cubic Bezier splines (open and closed, approximating and interpolating)\n* Evaluate and differentiate non-rational Bezier splines of any degree\n\n### this package will not**\n\n* Work with rational Bezier splines, b-splines, NURBS, or any other generalization of Bezier curves\n* Decrease curve degree\n* Approximate curve intersections\n* Approximate the length of a curve\n* "Stroke" (move left or right) a curve<br/>\n\n** much of the "will not" features can be found here: https://github.com/dhermes/bezier\n\n### Public classes / functions\n\n    # a c2-continuous cubic Bezier spline near the control points\n    new_open_approximating_spline([(x0, y0), (x1, y1), ...])\n\n    # a c2-continuous cubic Bezier spline near the control points\n    new_closed_approximating_spline([(x0, y0), (x1, y1), ...])\n\n    # a c2-continuous cubic Bezier spline through the control points\n    new_open_interpolating_spline([(x0, y0), (x1, y1), ...])\n\n    # a c2-continuous cubic Bezier spline through the control points\n    new_closed_interpolating_spline([(x0, y0), (x1, y1), ...])\n\nAny of these will return a BezierSpline object. This object has a some of the usual methods (e.g., elevate, derivative, split) to help find path normals or do some light modeling, but you may be most interested in.\n\n    # plot the spline at a given point, where time is 0 to\n    # (number of input points + 1)\n    spline(time: float)\n\n    # an svg data string\n    # (the d="" attribute of an SVG path object)\n    spline.svg_data\n\n### Examples\n\nSome of these use double and triple repeated points to create "knots". This isn\'t a special function, just a feature of Bezier math. The idea is clearer with a picture.\n\n![spline types](doc/knot_examples.png)\n\n### Most of the math can be found in:\n\n* A Primer on Bezier Curves<br/>\nhttps://pomax.github.io/bezierinfo/\n* UCLS-Math-149-Mathematics-of-Computer-Graphics-lecture-notes<br/>\nhttps://www.stkent.com/assets/pdfs/UCLA-Math-149-Mathematics-of-Computer-Graphics-lecture-notes.pdf\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
