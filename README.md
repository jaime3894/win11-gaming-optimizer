# Win11 Gaming Optimizer

Aplicación con GUI moderna para optimizar Windows 11 exclusivamente para gaming (Fortnite, Valorant, CS2, etc).

## Características

- **Dashboard** con info del sistema (CPU, GPU, RAM, Disco)
- **Sistema** — energía, servicios innecesarios, planificador, efectos visuales, HAGS
- **Red** — Nagle, throttling, DNS, QoS, system responsiveness
- **GPU** — pantalla completa, NVIDIA Low Latency, prioridad de GPU, MPO
- **Juegos** — perfiles de prioridad por juego (Fortnite, Valorant, CS2) + Game Mode
- **Avanzado** — Spectre/Meltdown, core parking, telemetría, IRQ priority
- **Restaurar** — todas las optimizaciones tienen un comando de reversión
- **Log de actividad** integrado en la app

## Requisitos

- Windows 11 (también funciona en Windows 10)
- Python 3.10+
- Privilegios de administrador (la app se auto-eleva al iniciar)

## Instalación

```powershell
cd C:\Users\jaime\win11-gaming-optimizer
pip install -r requirements.txt
```

## Uso

```powershell
python main.py
```

Al abrir la aplicación se solicitará permiso de administrador (UAC). Acepta para que las optimizaciones puedan modificar el registro y servicios de Windows.

### Flujo de trabajo recomendado

1. **Dashboard** — Verifica que el sistema se detectó correctamente.
2. **Sistema** — Comienza por aquí. Las optimizaciones marcadas por defecto son seguras y altamente recomendadas.
3. **Red** — Activa Nagle's Algorithm disabled y QoS si juegas online.
4. **GPU** — Aplica los tweaks aplicables a tu vendor (NVIDIA o AMD).
5. **Juegos** — Activa los perfiles de los juegos que tengas instalados.
6. **Avanzado** — Solo si sabes lo que haces. Lee cada descripción cuidadosamente.
7. Reinicia Windows para que todos los cambios surtan efecto.

### Indicadores de riesgo

- **BAJO** — cambios reversibles y bien documentados, seguros para cualquier PC.
- **MEDIO** — pueden afectar otras funciones (ej. cambiar DNS rompe redes corporativas).
- **ALTO** — debilitan la seguridad o son difíciles de revertir. Solo para PCs dedicadas a gaming.

## Estructura del proyecto

```
win11-gaming-optimizer/
├── main.py                    # Entry point (auto-elevación admin)
├── requirements.txt
└── app/
    ├── ui/
    │   ├── main_window.py     # Ventana principal con sidebar
    │   └── pages/             # Páginas por categoría
    ├── optimizations/
    │   ├── definitions.py     # Todas las optimizaciones (PowerShell)
    │   └── runner.py          # Ejecutor en thread
    └── utils/
        ├── admin.py           # Privilegios admin
        └── system_info.py     # Info de hardware
```

## Notas

- Todos los cambios al registro/servicios son reversibles vía botón **Restaurar**.
- La app ejecuta cada optimización como comando PowerShell aislado, capturando stdout/stderr al log.
- Los cambios de servicios y registro requieren reiniciar para tener efecto completo.

## Aviso

Este software modifica configuraciones críticas del sistema. Aunque todas las optimizaciones son reversibles, **se recomienda crear un punto de restauración del sistema antes de aplicar tweaks de la categoría Avanzado**.
