import EffectiveSection.EN1993_1_5.Sec4 as Sec4
import EffectiveSection.EN1993_1_3.Sec5_5_3 as Sec553
import EffectiveSection.Modes.IntCalcProp as intprop
import Definitions.Definitions as defin
import Constants.Constants as cons
import numpy as np
import matplotlib.pyplot as plt


def plotter(data: []):
    for i in data:
        x = [i[1], i[3]]
        y = [i[2], i[4]]
        t = i[5]
        plt.plot(x, y, linewidth=t * 2)
    plt.title('Bending About Weak Axis Lips are Under Compression | Effective Section')
    plt.axis('equal')
    plt.show()


class bendWeakLip:
    def __init__(self):
        # Variables for bending about strong axis
        self.BendWeakLip_xgct = None
        self.BendWeakLip_xgc = None
        self.BendWeakLip_elementData2 = None
        self.BendWeakLip_ygct = None  # Top flange extreme fiber to neutral axis
        self.BendWeakLip_ygc = None  # Bottom flange extreme fiber to neutral axis
        self.BendWeakLip_Iyeff = None  # Moment of inertia
        self.BendWeakLip_Wyeff = None  # Section modulus
        self.calcs_BendingWeakLip()
        self.Report = None

        # Section parts
        #         6       7
        #       ┌────   ────┐    ↑
        #       │           │ 8  │
        #       │ 5              hc
        #                        │
        #       │                ↓
        #     --│-------------------
        #       │
        #       │ 4
        #       │           │ 1
        #       └────   ────┘
        #          3      2

    def calcs_BendingWeakLip(self):
        # Design Stress
        scomed = defin.steel.fy
        Rep = f'{cons.secDivider}\nEFFECTIVE SECTION PROPERTIES \n  BENDING ABOUT WEAK AXIS \n  LIPS ARE UNDER COMPRESSION\n{cons.secDivider}\n'
        # ==============================================================================================================
        # Effective width of the top flange
        # ==============================================================================================================
        top_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        top_flg_ksigma = Sec4.Table4_2_ksigma(top_flg_stress_ratio, True)
        top_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, top_flg_ksigma, scomed, True)
        top_flg_rho = Sec4.internal_element(top_flg_lamp, top_flg_stress_ratio)
        top_flg_beff = Sec4.Table4_2_beff(defin.section.bb, top_flg_rho, top_flg_stress_ratio)[0]
        top_flg_be1 = defin.gross.zgx
        top_flg_be2 = top_flg_beff
        Rep += f'==== Effective width of the top flange ====\n'
        Rep += f'{cons.sp3}Stress ratio, Ψ = {top_flg_stress_ratio:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Buckling factor, kσ = {top_flg_ksigma:.3f}, EN 1993-1-5 Table 4.1.\n'
        Rep += f'{cons.sp3}Slenderness, λ = {top_flg_lamp:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Reduction factor, ρ = {top_flg_rho:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Effective width, be1 = {top_flg_be1:.3f}, EN 1993-1-5 Table 4.1.\n'
        Rep += f'{cons.sp3}Effective width, be2 = {top_flg_be2:.3f}, EN 1993-1-5 Table 4.1.\n'
        # ==============================================================================================================
        # Effective width of the bot flange
        # ==============================================================================================================
        bot_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        bot_flg_ksigma = Sec4.Table4_2_ksigma(bot_flg_stress_ratio, True)
        bot_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, bot_flg_ksigma, scomed, True)
        bot_flg_rho = Sec4.internal_element(bot_flg_lamp, bot_flg_stress_ratio)
        bot_flg_beff = Sec4.Table4_2_beff(defin.section.bb, bot_flg_rho, bot_flg_stress_ratio)[0]
        bot_flg_be1 = defin.gross.zgx
        bot_flg_be2 = bot_flg_beff
        Rep += f'==== Effective width of the bot flange ====\n'
        Rep += f'{cons.sp3}Stress ratio, Ψ = {bot_flg_stress_ratio:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Buckling factor, kσ = {bot_flg_ksigma:.3f}, EN 1993-1-5 Table 4.1.\n'
        Rep += f'{cons.sp3}Slenderness, λ = {bot_flg_lamp:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Reduction factor, ρ = {bot_flg_rho:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Effective width, be1 = {bot_flg_be1:.3f}, EN 1993-1-5 Table 4.1.\n'
        Rep += f'{cons.sp3}Effective width, be2 = {bot_flg_be2:.3f}, EN 1993-1-5 Table 4.1.\n'
        # ==============================================================================================================
        # Effective width of the top edge fold
        # ==============================================================================================================
        top_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        top_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        top_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, top_lip_ksigma, scomed, True)
        top_lip_rho = Sec4.outstand_element(top_lip_lamp)
        top_lip_beff = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[0]
        top_lip_bc = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[1]
        top_lip_bt = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        top_As = defin.section.tcore * (top_flg_be2 + top_lip_beff)
        # Spring stiffness of the edge stiffener
        top_b1 = Sec553.calc_b1(defin.section.bb, top_flg_be2, defin.section.tcore, top_lip_beff)
        top_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, top_b1, defin.section.aa,
                                        top_b1, False)
        top_Is = Sec553.Is(top_flg_be2, defin.section.tcore, top_lip_beff)
        top_scrs = Sec553.calc_scrs(top_K, top_Is, defin.steel.E, top_As)
        # Thickness reduction factor
        top_xd = Sec553.thk_reduction(scomed, top_scrs)
        top_t_red = top_xd * defin.section.tcore
        Rep += f'==== Effective width of the top edge fold ====\n'
        Rep += f'{cons.sp3}Stress ratio, Ψ = {top_lip_stres_ratio:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Buckling factor, kσ = {top_lip_ksigma:.3f}, EN 1993-1-3 Section 5.5.3.\n'
        Rep += f'{cons.sp3}Slenderness, λ = {top_lip_lamp:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Reduction factor, ρ = {top_lip_rho:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Effective width, beff = {top_lip_beff:.3f}, EN 1993-1-5 Table 4.2.\n'
        Rep += f'{cons.sp3}Effective area of the edge stiffener:\n As = {top_As:.3f}, EN 1993-1-3 Equation 5.14a.\n'
        Rep += f'{cons.sp3}Spring stiffness of the edge stiffener:\n b1 = {top_b1:.3f}, EN 1993-1-3 Section 5.5.3.1(5).\n'
        Rep += f'{cons.sp3}K = {top_K:.3f}, EN 1993-1-3 Equation 5.10b.\n'
        Rep += f'{cons.sp3}Is = {top_Is:.3f}, EN 1993-1-3 Equation 5.14a.\n'
        Rep += f'{cons.sp3}σcr,s = {top_scrs:.3f}, EN 1993-1-3 Equation 5.15a.\n'
        Rep += f'{cons.sp3}χd = {top_xd:.3f}, EN 1993-1-3 Section 5.5.3.1(7).\n'
        Rep += f'{cons.sp3}t,red = {top_t_red:.3f}, EN 1993-1-3 Section 5.5.3.2(6).\n'
        # ==============================================================================================================
        # Effective width of the bottom edge fold
        # ==============================================================================================================
        bot_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        bot_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        bot_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, bot_lip_ksigma, scomed, True)
        bot_lip_rho = Sec4.outstand_element(bot_lip_lamp)
        bot_lip_beff = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[0]
        bot_lip_bc = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[1]
        bot_lip_bt = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        bot_As = defin.section.tcore * (bot_flg_be2 + bot_lip_beff)
        # Spring stiffness of the edge stiffener
        bot_b1 = Sec553.calc_b1(defin.section.bb, bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, bot_b1, defin.section.aa,
                                        bot_b1, False)
        bot_Is = Sec553.Is(bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_scrs = Sec553.calc_scrs(bot_K, bot_Is, defin.steel.E, bot_As)
        # Thickness reduction factor
        bot_xd = Sec553.thk_reduction(scomed, bot_scrs)
        bot_t_red = bot_xd * defin.section.tcore
        Rep += f'==== Effective width of the bottom edge fold ====\n'
        Rep += f'{cons.sp3}Stress ratio, Ψ = {bot_lip_stres_ratio:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Buckling factor, kσ = {bot_lip_ksigma:.3f}, EN 1993-1-3 Section 5.5.3.\n'
        Rep += f'{cons.sp3}Slenderness, λ = {bot_lip_lamp:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Reduction factor, ρ = {bot_lip_rho:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Effective width, beff = {bot_lip_beff:.3f}, EN 1993-1-5 Table 4.2.\n'
        Rep += f'{cons.sp3}Effective area of the edge stiffener:\n As = {bot_As:.3f}, EN 1993-1-3 Equation 5.14a.\n'
        Rep += f'{cons.sp3}Spring stiffness of the edge stiffener:\n b1 = {bot_b1:.3f}, EN 1993-1-3 Section 5.5.3.1(5).\n'
        Rep += f'{cons.sp3}K = {bot_K:.3f}, EN 1993-1-3 Equation 5.10b.\n'
        Rep += f'{cons.sp3}Is = {bot_Is:.3f}, EN 1993-1-3 Equation 5.14a.\n'
        Rep += f'{cons.sp3}σcr,s = {bot_scrs:.3f}, EN 1993-1-3 Equation 5.15a.\n'
        Rep += f'{cons.sp3}χd = {bot_xd:.3f}, EN 1993-1-3 Section 5.5.3.1(7).\n'
        Rep += f'{cons.sp3}t,red = {bot_t_red:.3f}, EN 1993-1-3 Section 5.5.3.2(6).\n'
        # ==============================================================================================================
        # Effective width of the web
        # ==============================================================================================================
        # Web is fully effective under tension
        ff = 1.0
        web_ksigma = Sec4.Table4_1_ksigma(ff)
        web_lamp = Sec4.lamp(defin.section.aa, defin.section.tcore, web_ksigma, scomed, False)
        web_rho = Sec4.internal_element(web_lamp, ff)
        web_beff = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[0]
        web_be1 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[1]
        web_be2 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[2]
        h1 = web_be1
        h2 = web_be1
        Rep += f'==== Effective width of the web ====\n'
        Rep += f'{cons.sp3}Web is fully effective under tension.\n'
        Rep += f'{cons.sp3}Stress ratio, Ψ = {ff:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Slenderness, λ = {web_lamp:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Reduction factor, ρ = {web_rho:.3f}, EN 1993-1-5 Section 4.\n'
        Rep += f'{cons.sp3}Effective width, be1 = {h1:.3f}, EN 1993-1-5 Table 4.1.\n'
        Rep += f'{cons.sp3}Effective width, be2 = {h2:.3f}, EN 1993-1-5 Table 4.1.\n'
        # ==============================================================================================================
        # Effective section properties
        # ==============================================================================================================
        # Create a matrix contains the element data from bottom lip to top lip
        # 0 id , 1 inodeX, 2 inodeY, 3 jnodeX, 4 JnodeY, 5 thickness
        self.BendWeakLip_elementData2 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [4, 0.0, 0.0, 0.0, h2, defin.section.tcore],
             [5, 0.0, defin.section.aa - h1, 0.0, defin.section.aa, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])

        # Plot the shape
        # plotter(self.BendWeakLip_elementData2)

        # Results
        self.BendWeakLip_Iyeff = intprop.calcProps(self.BendWeakLip_elementData2)[4]
        self.BendWeakLip_xgc = intprop.calcProps(self.BendWeakLip_elementData2)[3]
        self.BendWeakLip_xgct = defin.section.bb - intprop.calcProps(self.BendWeakLip_elementData2)[3]
        self.BendWeakLip_Wyeff = intprop.calcProps(self.BendWeakLip_elementData2)[4] / (
            max(self.BendWeakLip_xgc, self.BendWeakLip_xgct))
        Rep += f'==== Effective properties ====\n'
        Rep += f'{cons.sp3}Distance from bottom flange:\n xgc = {self.BendWeakLip_xgc:.3f} mm.\n'
        Rep += f'{cons.sp3}Distance from top flange:\n xgct = {self.BendWeakLip_xgct:.3f} mm.\n'
        Rep += f'{cons.sp3}Effective second moment of area:\n Ieff = {self.BendWeakLip_Iyeff:.3f} mm⁴.\n'
        Rep += f'{cons.sp3}Effective section modulus (min):\n Weff = {self.BendWeakLip_Wyeff:.3f} mm³.\n\n'
        self.Report = Rep
        print(self.Report)
