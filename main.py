from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# =================================================================
# Inicializa FastAPI
# =================================================================
app = FastAPI(
    title="Análisis de Muros de Mampostería",
    description="Una aplicación web para generar el diagrama de interacción de muros de mampostería.",
    version="1.1.0"
)

# Configura Jinja2 para cargar plantillas HTML
templates = Jinja2Templates(directory="templates")


# =================================================================
# Función para realizar los cálculos
# =================================================================
def perform_calculations(
    C1_h_muro_m, C2_L_muro_m, C3_em_base_mampost_cm, C4_lm_largo_mampost_cm,
    C5_e_separacion_mamp_cm, C6_e_mampost_cm, C24_b_conf_cm, C25_h_conf_cm,
    C10_fy_kg_cm2, C18_fc_kg_cm2, C21_fm_kg_cm2, C51_emu, C60_Es_kg_cm2,
    C11_fi_mm, C12_Nvar_x, C13_Nvar_y, C52_recubrimiento_cm, C53_fiestrib_mm
):
    """
    Realiza los cálculos del diagrama de interacción.
    """
    # =================================================================
    # 2. CÁLCULOS PRELIMINARES
    # =================================================================
    C7_h_celda_cm = C3_em_base_mampost_cm - C6_e_mampost_cm * 2
    C14_Ntotal = (C12_Nvar_x * 2) + (C13_Nvar_y - 2) * 2
    C15_As_cm2 = (np.pi * C11_fi_mm**2 * C14_Ntotal) / (4 * 10**2)
    C26_Area_cm2 = C24_b_conf_cm * C25_h_conf_cm
    C29_yc_cm = C3_em_base_mampost_cm / 2
    C30_xc_cm = C4_lm_largo_mampost_cm / 2
    C57_Lmuro_cm = C2_L_muro_m * 100
    D35, E35 = C4_lm_largo_mampost_cm, C6_e_mampost_cm
    F35_Area1 = E35 * D35
    G35_y1 = C3_em_base_mampost_cm - E35 / 2
    H35_Io1 = (D35 * E35**3) / 12
    I35_d1 = C3_em_base_mampost_cm / 2 - G35_y1
    J35_Ixc1 = H35_Io1 + F35_Area1 * I35_d1**2
    D36, E36 = C4_lm_largo_mampost_cm, C6_e_mampost_cm
    F36_Area2 = E36 * D36
    G36_y2 = E36/2
    I36_d2 = C3_em_base_mampost_cm / 2 - G36_y2
    H36_Io2 = (D36 * E36**3) / 12
    J36_Ixc2 = H36_Io2 + F36_Area2 * I36_d2**2
    C38_Area_total_mamp = F35_Area1 + F36_Area2
    C39_Inercia_total_mamp = J35_Ixc1 + J36_Ixc2
    C40_radio_giro_r = np.sqrt(C39_Inercia_total_mamp / C38_Area_total_mamp)
    C67_h_muro_cm = C1_h_muro_m * 100
    C43_esbeltez_h_r = C67_h_muro_cm / C40_radio_giro_r
    if C43_esbeltez_h_r <= 99:
        C70_facte = 1 - (C67_h_muro_cm / (140 * C40_radio_giro_r))**2
    else:
        C70_facte = ((70 * C40_radio_giro_r) / C67_h_muro_cm)**2
    C46 = (C4_lm_largo_mampost_cm - 2 * C6_e_mampost_cm -
           C5_e_separacion_mamp_cm) * C7_h_celda_cm
    C47 = C38_Area_total_mamp + C7_h_celda_cm * C6_e_mampost_cm * \
        2 + C7_h_celda_cm * C5_e_separacion_mamp_cm
    C54_An_cm2 = C47 * (C57_Lmuro_cm / C4_lm_largo_mampost_cm)
    C55_As_final = C15_As_cm2
    C56_separacion_var_cm = (C24_b_conf_cm - 2 * C52_recubrimiento_cm - C11_fi_mm /
                             10 - (C53_fiestrib_mm/10)*2) / (C12_Nvar_x-1 if C12_Nvar_x > 1 else 1)
    C58_fm_final = C21_fm_kg_cm2
    C59_fy_final = C10_fy_kg_cm2
    C61_d_peralte_efectivo = C57_Lmuro_cm - C52_recubrimiento_cm - \
        C53_fiestrib_mm/10 - C11_fi_mm/20
    C62_cd_balanceado = C51_emu / (C51_emu + C59_fy_final / C60_Es_kg_cm2)
    C63_cd_t_controlada = 1/3
    C64_cd_alta_ductilidad = 1/4
    C65_cd_flex_pura = ((C55_As_final * C59_fy_final * C57_Lmuro_cm) /
                        (0.8 * C58_fm_final * 0.8 * C54_An_cm2)) / C61_d_peralte_efectivo
    C73, D73, E73, F73, G73 = 1, 2, 3, 4, 5
    H73, I73, J73, K73, L73 = 1, 2, 3, 4, 5
    d_steel = np.zeros(10)
    As_layers = np.zeros(10)
    if C12_Nvar_x >= C73:
        d_steel[0] = C52_recubrimiento_cm + \
            C53_fiestrib_mm/10 + C11_fi_mm/20
    if C12_Nvar_x >= C73:
        As_layers[0] = C55_As_final/C14_Ntotal * C13_Nvar_y
    if C12_Nvar_x >= D73:
        d_steel[1] = d_steel[0] + C56_separacion_var_cm
    if C12_Nvar_x >= D73:
        As_layers[1] = (C55_As_final/C14_Ntotal * 2) if C12_Nvar_x > D73 else (
            C55_As_final/C14_Ntotal * C13_Nvar_y)
    if C12_Nvar_x >= E73:
        d_steel[2] = d_steel[1] + C56_separacion_var_cm
    if C12_Nvar_x >= E73:
        As_layers[2] = (C55_As_final/C14_Ntotal * 2) if C12_Nvar_x > E73 else (
            C55_As_final/C14_Ntotal * C13_Nvar_y)
    if C12_Nvar_x >= H73:
        d_steel[5] = C57_Lmuro_cm - C24_b_conf_cm + d_steel[0]
    if C12_Nvar_x >= H73:
        As_layers[5] = C55_As_final/C14_Ntotal * C13_Nvar_y
    if C12_Nvar_x >= I73:
        d_steel[6] = C57_Lmuro_cm - C24_b_conf_cm + d_steel[1]
    if C12_Nvar_x >= I73:
        As_layers[6] = (C55_As_final/C14_Ntotal * 2) if C12_Nvar_x > I73 else (
            C55_As_final/C14_Ntotal * C13_Nvar_y)
    if C12_Nvar_x >= J73:
        d_steel[7] = C57_Lmuro_cm - C24_b_conf_cm + d_steel[2]
    if C12_Nvar_x >= J73:
        As_layers[7] = (C55_As_final/C14_Ntotal * 2) if C12_Nvar_x > J73 else (
            C55_As_final/C14_Ntotal * C13_Nvar_y)
    mask = As_layers > 0
    d_steel_final = d_steel[mask]
    As_layers_final = As_layers[mask]
    d_centroide = C57_Lmuro_cm / 2

    # =================================================================
    # 3. RECREACIÓN DE LA TABLA DE CÁLCULO
    # =================================================================
    c_d_fijos = [1.0125, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55,
                 0.50, 0.45, 0.40, 0.35, 0.30, 0.20, 0.10, 0.01]
    c_d_calculados = [C62_cd_balanceado, C63_cd_t_controlada,
                      C64_cd_alta_ductilidad, C65_cd_flex_pura]
    c_d_relacion = sorted(list(set(c_d_fijos + c_d_calculados)), reverse=True)
    df = pd.DataFrame()
    df['B_relacion_c_d'] = c_d_relacion
    df['c'] = df['B_relacion_c_d'] * C61_d_peralte_efectivo
    df['Cm_kg'] = 0.8 * C54_An_cm2 * \
        ((0.8 * df['c']) / C57_Lmuro_cm) * C58_fm_final
    momentos_acero_cols = []
    fuerzas_acero_cols = []
    for i in range(len(d_steel_final)):
        condicion1 = C57_Lmuro_cm - d_steel_final[i] >= df['c']
        condicion2 = d_steel_final[i] != 0
        df[f'est_{i+1}'] = np.where(
            condicion1 & condicion2,
            C51_emu * ((C57_Lmuro_cm - d_steel_final[i] - df['c']) / df['c']),
            0
        )
        df[f'fs_{i+1}'] = df[f'est_{i+1}'] * C60_Es_kg_cm2
        df[f'fs_{i+1}'] = np.clip(df[f'fs_{i+1}'], -C59_fy_final, C59_fy_final)
        df[f'T_{i+1}'] = df[f'fs_{i+1}'] * As_layers_final[i]
        fuerzas_acero_cols.append(f'T_{i+1}')
        df[f'M_{i+1}'] = df[f'T_{i+1}'] * (d_centroide - d_steel_final[i])
        momentos_acero_cols.append(f'M_{i+1}')
    df['Facero_kg'] = df[fuerzas_acero_cols].sum(axis=1)
    df['Mcm_kgcm'] = df['Cm_kg'] * (d_centroide - 0.8 * df['c'] / 2)
    df['Macero_kgcm'] = df[momentos_acero_cols].sum(axis=1)
    phi = 0.9
    df['Mr_kgcm'] = phi * (df['Mcm_kgcm'] + df['Macero_kgcm'])
    df['Pr_kg'] = phi * C70_facte * (df['Cm_kg'] - df['Facero_kg'])
    df['Mr_Tm'] = df['Mr_kgcm'] / 100000
    df['Pr_T'] = df['Pr_kg'] / 1000
    df.loc[df.index[0], 'Mr_Tm'] = 0
    df.loc[df.index[-1], 'Mr_Tm'] = 0

    # =================================================================
    # 4. GENERACIÓN DE GRÁFICAS
    # =================================================================
    # --- Gráfica 1: Diagrama de Interacción ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig_diagram, ax_diagram = plt.subplots(figsize=(10, 8))
    ax_diagram.plot(df['Mr_Tm'], df['Pr_T'], marker='o', linestyle='-',
                    color='blue', label='Capacidad del Muro (Python)')
    ax_diagram.set_title('Diagrama de Interacción',
                         fontsize=16, fontweight='bold')
    ax_diagram.set_xlabel('Momento Resistente (Mr) [T-m]', fontsize=12)
    ax_diagram.set_ylabel('Carga Resistente (Pr) [T]', fontsize=12)
    ax_diagram.axhline(0, color='black', linewidth=0.7)
    ax_diagram.axvline(0, color='black', linewidth=0.7)
    ax_diagram.legend()
    ax_diagram.grid(True)
    min_carga = df['Pr_T'].min()
    if min_carga < 0:
        ax_diagram.set_ylim(bottom=min_carga * 1.1)

    # Convertir la gráfica a base64
    buf = io.BytesIO()
    fig_diagram.savefig(buf, format='png')
    buf.seek(0)
    diagram_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig_diagram)

    # Preparar el dataframe para la salida
    tabla_comparativa = df[['B_relacion_c_d', 'Mr_Tm', 'Pr_T']].copy()
    tabla_comparativa.rename(columns={
        'B_relacion_c_d': 'Relación c/d',
        'Mr_Tm': 'Momento Resistente (T-m)',
        'Pr_T': 'Carga Resistente (T)'
    }, inplace=True)

    return {
        "diagram_b64": diagram_b64,
        "results_df": tabla_comparativa.to_html(classes='dataframe', index=False, float_format='{:.4f}'.format)
    }


# =================================================================
# Endpoints de la API
# =================================================================
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """
    Muestra el formulario de ingreso de datos.
    """
    return templates.TemplateResponse("index.html", {"request": request, "results": None, "inputs": None})


@app.post("/", response_class=HTMLResponse)
async def calculate_from_form(
    request: Request,
    C1_h_muro_m: float = Form(...),
    C2_L_muro_m: float = Form(...),
    C3_em_base_mampost_cm: float = Form(...),
    C4_lm_largo_mampost_cm: float = Form(...),
    C5_e_separacion_mamp_cm: float = Form(...),
    C6_e_mampost_cm: float = Form(...),
    C24_b_conf_cm: float = Form(...),
    C25_h_conf_cm: float = Form(...),
    C10_fy_kg_cm2: float = Form(...),
    C18_fc_kg_cm2: float = Form(...),
    C21_fm_kg_cm2: float = Form(...),
    C51_emu: float = Form(...),
    C60_Es_kg_cm2: float = Form(...),
    C11_fi_mm: float = Form(...),
    C12_Nvar_x: int = Form(...),
    C13_Nvar_y: int = Form(...),
    C52_recubrimiento_cm: float = Form(...),
    C53_fiestrib_mm: float = Form(...)
):
    """
    Recibe los datos del formulario, realiza los cálculos y muestra los resultados.
    """
    calculation_results = perform_calculations(
        C1_h_muro_m, C2_L_muro_m, C3_em_base_mampost_cm, C4_lm_largo_mampost_cm,
        C5_e_separacion_mamp_cm, C6_e_mampost_cm, C24_b_conf_cm, C25_h_conf_cm,
        C10_fy_kg_cm2, C18_fc_kg_cm2, C21_fm_kg_cm2, C51_emu, C60_Es_kg_cm2,
        C11_fi_mm, C12_Nvar_x, C13_Nvar_y, C52_recubrimiento_cm, C53_fiestrib_mm
    )

    input_data = {
        "C1_h_muro_m": C1_h_muro_m, "C2_L_muro_m": C2_L_muro_m,
        "C3_em_base_mampost_cm": C3_em_base_mampost_cm,
        "C4_lm_largo_mampost_cm": C4_lm_largo_mampost_cm,
        "C5_e_separacion_mamp_cm": C5_e_separacion_mamp_cm,
        "C6_e_mampost_cm": C6_e_mampost_cm,
        "C24_b_conf_cm": C24_b_conf_cm, "C25_h_conf_cm": C25_h_conf_cm,
        "C10_fy_kg_cm2": C10_fy_kg_cm2, "C18_fc_kg_cm2": C18_fc_kg_cm2,
        "C21_fm_kg_cm2": C21_fm_kg_cm2, "C51_emu": C51_emu,
        "C60_Es_kg_cm2": C60_Es_kg_cm2, "C11_fi_mm": C11_fi_mm,
        "C12_Nvar_x": C12_Nvar_x, "C13_Nvar_y": C13_Nvar_y,
        "C52_recubrimiento_cm": C52_recubrimiento_cm,
        "C53_fiestrib_mm": C53_fiestrib_mm
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": calculation_results,
        "inputs": input_data
    })


# =================================================================
# Ejecución para desarrollo local
# =================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
