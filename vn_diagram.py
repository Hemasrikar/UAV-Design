import numpy as np
import matplotlib.pyplot as plt

def VN(aircraft):
    # Conversions
    fps_per_knot = 1.6878
    g = 32.2

    # Data Setup
    h = aircraft['h']
    W = aircraft['W']
    CLmax = aircraft['CLmax']
    Sref = aircraft['Sref']
    DesignLoadFactor = aircraft['DesignLoadFactor']
    Vne = aircraft['Vne']
    Cla = aircraft['Cla']
    mean_geom_chord = aircraft['mean_geom_chord']

    Vpoints = 100
    Vbuffer = 0.1 * Vne  # kts
    Nbuffer = 0.5  # g

    if min(DesignLoadFactor) > 0:
        # warning('Minimum Design Load Factor should be 0 or lower')
        pass

    speed_kts = np.linspace(0, Vne, num=Vpoints)  # kts
    Vne_fps = Vne * fps_per_knot  # ft/s
    speed_fps = np.linspace(0, Vne_fps, num=Vpoints)  # ft/s

    # Gust Line Setup
    Vg = np.array([25, 12, 6])  # ft/s [VB VC VD] gust magnitude

    # Plot Setup
    plt.figure(figsize=(10, 6))
    plt.xlim(0, Vne + Vbuffer)
    plt.ylim(min(min(DesignLoadFactor) - Nbuffer, -1), max(DesignLoadFactor) + Nbuffer)
    plt.grid(True)
    plt.xlabel('Indicated Airspeed (kts)')
    plt.ylabel('Load Factor (g)')
    plt.title('Flight Envelope (V-n Diagram)')

    # Output Parameter Setup
    Vstall_pos = []
    Va_pos = []
    Vstall_neg = []
    Va_neg = []

    n_gust_pos = np.zeros((len(Vg), Vpoints))
    n_gust_neg = np.zeros((len(Vg), Vpoints))

    # Stall line calculations
    for alt in h:
        # plot one line for each altitude requested
        rho = stdatm(alt, "R", 1)  # density slug/ft^3
        density_ratio = stdatm(alt, "RR", 1)

        # convert IAS to TAS
        speed_fps_true = np.sqrt(speed_fps ** 2 / density_ratio)

        for weight in W:
            # plot one line for each Weight configuration

            # calculate positive stall line
            n_pos = np.maximum.reduce(CLmax) * Sref * rho * speed_fps_true ** 2 / (2 * weight)

            # calculate negative stall line
            if len(CLmax) > 1:
                n_neg = np.minimum.reduce(CLmax) * Sref * rho * speed_fps_true ** 2 / (2 * weight)

            else:
                n_neg = np.zeros_like(speed_fps)

            # calculate gust lines
            for j in range(len(Vg)):
                mu = 2 * weight / (Sref * rho * mean_geom_chord * Cla * g)
                Kg = 0.88 * mu / (5.3 + mu)
                n_gust_pos[j, :] = 1 + (Kg * Cla * Vg[j] * speed_kts) / (498 * weight / Sref)
                n_gust_neg[j, :] = 1 - (Kg * Cla * Vg[j] * speed_kts) / (498 * weight / Sref)

            # Find Stall Speed
            Vstall_pos.append(np.interp(1, n_pos, speed_kts))
            Vstall_neg.append(np.interp(-1, n_neg, speed_kts))

            # truncate stall lines to limit loads
            n_pos[n_pos > max(DesignLoadFactor)] = max(DesignLoadFactor)
            n_neg[n_neg < min(DesignLoadFactor)] = min(DesignLoadFactor)

            # Find Maneuver Speed
            Va_pos.append(np.max(speed_kts[n_pos < max(DesignLoadFactor)]))
            Va_neg.append(np.max(speed_kts[n_neg > min(DesignLoadFactor)]))

            # plot the envelope lines
            plt.plot(speed_kts, n_pos, color='blue', linewidth=2)
            plt.plot(speed_kts, n_neg, color='blue', linewidth=2)

            # plot Vne line
            plt.plot([Vne, Vne], [max(n_pos), min(n_neg)], color='blue', linewidth=2)

            # plot Gust lines
            for j in range(len(Vg)):
                if j == 0:
                    plt.plot(speed_kts, n_gust_pos[j, :], color='green', linestyle='-.', linewidth=2, label='Gust Lines')
                else:
                    plt.plot(speed_kts, n_gust_pos[j, :], color='green', linestyle='-.', linewidth=2)
                plt.plot(speed_kts, n_gust_neg[j, :], color='green', linestyle='-.', linewidth=2)
            plt.legend()

    # Clean up output parameters because we had a leading placeholder value
    Vstall_pos = Vstall_pos[1:]
    Va_pos = Va_pos[1:]
    Vstall_neg = Vstall_neg[1:]
    Va_neg = Va_neg[1:]

    # plot Vs lines
    for i in range(len(Vstall_pos)):
        plt.plot([Vstall_pos[i], Vstall_pos[i]], [0, 1], color='red', linewidth=1)
        plt.plot([Vstall_neg[i], Vstall_neg[i]], [0, -1], color='red', linewidth=1)

    # plot Va lines
    for i in range(len(Va_pos)):
        if Va_pos[i] < Vne:
            plt.plot([Va_pos[i], Va_pos[i]], [0, max(DesignLoadFactor)], color='blue', linewidth=1)
        if Va_neg[i] < Vne:
            plt.plot([Va_neg[i], Va_neg[i]], [0, min(DesignLoadFactor)], color='blue', linewidth=1)

    plt.xticks(range(0, 51, 5))
    plt.yticks(np.arange(-2, 4, 0.5))
    plt.grid(True, linestyle='dashed')
    plt.show()


def stdatm(Z, param="all", k=1):
    # Based on stdatm.m from: http://www.dept.aoe.vt.edu/~mason/Mason_f/MRsoft.html
    # k=0 for metric, 1 for std
    #     Z  - input altitude, in feet or meters (depending on k)
    #
    #     output:
    #                      units: metric        English
    #     T  - temp.               deg K         deg R
    #     P  - pressure            N/m^2         lb/ft^2
    #     R  - density (rho)       Kg/m^3        slug/ft^3
    #     A  - speed of sound      m/sec         ft/sec
    #     MU - viscosity           Kg/(m sec)    slug/(ft sec)
    #     TS - t/t at sea level
    #     RR - rho/rho at sea level
    #     PP - p/p at sea level
    #     RM - Reynolds number per Mach per unit of length
    #     QM - dynamic pressure/Mach^2

    KK = 0
    K = 34.163195
    C1 = 3.048e-4
    T = 1
    PP = 0

    if k == 0:
        TL = 288.15
        PL = 101325
        RL = 1.225
        C1 = 0.001
        AL = 340.294
        ML = 1.7894e-5
        BT = 1.458e-6
    else:
        TL = 518.67
        PL = 2116.22
        RL = 0.0023769
        AL = 1116.45
        ML = 3.7373e-7
        BT = 3.0450963e-8

    H = C1 * Z / (1 + C1 * Z / 6356.766)

    if H < 11:
        T = 288.15 - 6.5 * H
        PP = (288.15 / T) ** (-K / 6.5)
    elif H < 20:
        T = 216.65
        PP = 0.22336 * np.exp(-K * (H - 11) / 216.65)
    elif H < 32:
        T = 216.65 + (H - 20)
        PP = 0.054032 * (216.65 / T) ** K
    elif H < 47:
        T = 228.65 + 2.8 * (H - 32)
        PP = 0.0085666 * (228.65 / T) ** (K / 2.8)
    elif H < 51:
        T = 270.65
        PP = 0.0010945 * np.exp(-K * (H - 47) / 270.65)
    elif H < 71:
        T = 270.65 - 2.8 * (H - 51)
        PP = 0.00066063 * (270.65 / T) ** (-K / 2.8)
    elif H < 84.852:
        T = 214.65 - 2 * (H - 71)
        PP = 3.9046e-5 * (214.65 / T) ** (-K / 2)

    M1 = np.sqrt(1.4 * 287 * T)
    RR = PP / (T / 288.15)
    MU = BT * T ** 1.5 / (T + 110.4)
    TS = T / 288.15
    A = AL * np.sqrt(TS)
    T = TL * TS
    R = RL * RR
    P = PL * PP
    RM = R * A / MU
    QM = 0.7 * P

    if param == "all":
        return {'T': T, 'P': P, 'R': R, 'A': A, 'MU': MU, 'TS': TS, 'RR': RR, 'PP': PP, 'RM': RM, 'QM': QM}
    elif param in ['T', 'P', 'R', 'A', 'MU', 'TS', 'RR', 'PP', 'RM', 'QM']:
        return locals()[param]


# Data Setup

# Vmax = 24 m/s
# platform_area = 1.5 m^2
# Cl_max = 1.5
# Total_weight =  21.98kg
# mean_chord = 0.48m

uav = {

'h': [0],
'W': [21.98*2.20462],
'CLmax': [-1.5,1.5],
'Sref': 1.5*10.7639 ,
'DesignLoadFactor': [-1.5,3],
'Vne': 24*1.94384,
'Cla': 0.2 * 180 / np.pi,
'mean_geom_chord': 0.425* 3.28084

}

VN(uav)

