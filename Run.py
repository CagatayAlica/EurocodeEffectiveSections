import Definitions.Definitions as defin
import EffectiveSection.Modes.AxialCompression as axial
import EffectiveSection.Modes.BendingStrong as bendStr
import EffectiveSection.Modes.BendingWeakLip as benWeakLip
import EffectiveSection.Modes.BendingWeakWeb as benWeakWeb


def runEffective():
    Eff_Axial = axial.AxialComp(defin.steel.fy)
    Eff_BendingStrong = bendStr.bendStrong()
    Eff_BendingWeakLip = benWeakLip.bendWeakLip()
    Eff_BendingWeakWeb = benWeakWeb.bendWeakWeb()

    # Summary
    Summary = (f'==== SUMMARY ====\n'
               f'Aeff = {Eff_Axial.Axial_Aeff:.3f} mm². Effective cross section area under axial compression.\n'
               f'Weff = {Eff_BendingStrong.BendStrong_Wxeff:.3f} mm³. Effective section modulus under bending about strong axis.\n'
               f'Weff = {Eff_BendingWeakLip.BendWeakLip_Wyeff:.3f} mm³. Effective section modulus under bending about weak axis. Lips are under compression.\n'
               f'Weff = {Eff_BendingWeakWeb.BendWeakWeb_Wyeff:.3f} mm³. Effective section modulus under bending about weak axis. Web is under compression.\n')
    print(Summary)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runEffective()
