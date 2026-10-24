from datetime import date

def _validar_fecha(fecha):
    if isinstance(fecha, date):
        return fecha
    else:
        return date.fromisoformat(fecha)

def _filtrar_pedidos_confirmados(pedidos, fecha_inicio, fecha_fin):
    return [p for p in pedidos if p.estado == "CONFIRMADO" and fecha_inicio <= p.fecha.date() <= fecha_fin]

def _generar_estadisticas(pedidos):
    total = 0
    cantidad = 0
    premium = 0
    corporativo = 0
    normal = 0

    for p in pedidos:
        total += p.total_pagado
        cantidad += 1
        if p.cliente.tipo == "PREMIUM":
            premium += 1
        elif p.cliente.tipo == "CORPORATIVO":
            corporativo += 1
        else:
            normal += 1

    promedio = total / cantidad if cantidad > 0 else 0

    return total, cantidad, promedio, normal, premium, corporativo

def generar_reporte_ventas(pedidos, fecha_inicio, fecha_fin, incluir_detalle=False):

    fi = _validar_fecha(fecha_inicio)
    ff = _validar_fecha(fecha_fin)
    datos = _filtrar_pedidos_confirmados(pedidos, fi, ff)

    total, cantidad, promedio, normal, premium, corporativo = _generar_estadisticas(datos)

    salida = ""
    salida = salida + "REPORTE DE VENTAS\n"
    salida = salida + "=================\n"
    salida = salida + f"Desde: {fi.isoformat()}\n"
    salida = salida + f"Hasta: {ff.isoformat()}\n"
    salida = salida + f"Pedidos confirmados: {cantidad}\n"
    salida = salida + f"Total vendido: ${total:,.0f}\n"
    salida = salida + f"Promedio por pedido: ${promedio:,.0f}\n"
    salida = salida + f"Clientes NORMAL: {normal}\n"
    salida = salida + f"Clientes PREMIUM: {premium}\n"
    salida = salida + f"Clientes CORPORATIVO: {corporativo}\n"

    if incluir_detalle:
        salida = salida + "\nDETALLE\n"
        salida = salida + "-------\n"
        for p in datos:
            salida = salida + (
                f"{p.id} | {p.cliente.nombre} | "
                f"{p.ciudad} | ${p.total_pagado:,.0f}\n"
            )

    if cantidad == 0:
        salida = salida + "\nNo se encontraron ventas para el período.\n"

    return salida
