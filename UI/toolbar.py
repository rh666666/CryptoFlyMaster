from main import ui_keyed_sub, ui_vegenere, ui_playfair, ui_affine, ui_hill

def activate(win, ui):
    ui = ui
    win = win
    win.keyed_sub = ui_keyed_sub()
    win.affine = ui_affine()
    win.vegenere = ui_vegenere()
    win.playfair = ui_playfair()
    win.hill = ui_hill()
    ui.actionKeyedsub.triggered.connect(win.keyed_sub.show)
    ui.actionAffine.triggered.connect(win.affine.show)
    ui.actionVegenere.triggered.connect(win.vegenere.show)
    ui.actionPlayfair.triggered.connect(win.playfair.show)
    ui.actionHill.triggered.connect(win.hill.show)