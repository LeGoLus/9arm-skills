"""Layout checks in render.py:  cd scripts && uv run --with pytest pytest -q test_render.py"""
from render import lines_over_text, text_over_borders


def rect(i, x, y, w, h, t="rectangle"):
    return {"id": i, "type": t, "x": x, "y": y, "width": w, "height": h}


def text(i, x, y, w, h, s="label", **k):
    return {"id": i, "type": "text", "x": x, "y": y, "width": w, "height": h, "text": s, **k}


def scene(*els):
    return {"elements": list(els)}


def test_text_fully_inside_a_box_is_fine():
    assert text_over_borders(scene(rect("zone", 0, 0, 400, 300), text("t", 20, 20, 200, 30))) == []


def test_text_fully_outside_a_box_is_fine():
    assert text_over_borders(scene(rect("zone", 0, 0, 400, 300), text("t", 420, 20, 100, 30))) == []


def test_text_across_a_box_edge_is_flagged():
    found = text_over_borders(scene(rect("zone", 0, 0, 400, 300), text("t", 350, 100, 150, 30, "② NAS ดึง")))
    assert len(found) == 1 and "zone" in found[0] and "t" in found[0]


def test_text_bound_to_its_own_container_is_ignored():
    s = scene(rect("box", 0, 0, 100, 40), text("t", -10, 5, 120, 30, containerId="box"))
    assert text_over_borders(s) == []


def test_ellipse_edges_count_too():
    found = text_over_borders(scene(rect("c", 100, 100, 64, 64, "ellipse"), text("t", 140, 110, 120, 20)))
    assert found


def test_text_inside_one_zone_and_beside_a_circle_is_fine():
    s = scene(rect("zone", 0, 0, 600, 400), rect("c", 100, 100, 64, 64, "ellipse"), text("t", 80, 176, 104, 20))
    assert text_over_borders(s) == []


def test_lines_over_text_still_reports_crossings():
    line = {"id": "a", "type": "arrow", "x": 0, "y": 50, "points": [[0, 0], [300, 0]]}
    assert lines_over_text(scene(line, text("t", 100, 40, 80, 20)))
