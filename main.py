
class userInputs:
    def __init__(self):
        self.fy = None
        self.R = None
        self.t = None
        self.C = None
        self.B = None
        self.A = None
        self.inputs()

    def inputs(self):
        # Main inputs for the calculations:
        # ==== Sections ====
        self.A: float = 90.0
        self.B: float = 45.0
        self.C: float = 15.0
        self.t: float = 1.2
        self.R: float = 2.5
        # ==== Material ====
        self.fy: float = 350.0

        secDivider = '============================================'
        Rep = f'{secDivider}\nUSER INPUT\n{secDivider}\n'
        Rep += f'==== Sections ====\n'
        Rep += f'A = {self.A:.2f} mm\n'
        Rep += f'B = {self.B:.2f} mm\n'
        Rep += f'C = {self.C:.2f} mm\n'
        Rep += f't = {self.t:.2f} mm\n'
        Rep += f'R = {self.R:.2f} mm\n'
        Rep += f'==== Material ====\n'
        Rep += f'fy = {self.fy:.2f} MPa\n'

        print(Rep)

