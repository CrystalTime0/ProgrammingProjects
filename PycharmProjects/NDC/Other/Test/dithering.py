import pyxel

def draw():
    pyxel.cls(0)

    pyxel.dither(1.0)
    pyxel.rect(10, 10, 50, 50, 8)  # carré plein

    pyxel.dither(0.5)
    pyxel.rect(70, 10, 50, 50, 8)  # carré avec dithering

pyxel.init(130, 70)
pyxel.run(lambda: None, draw)
