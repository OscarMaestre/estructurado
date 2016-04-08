#!/usr/bin/env python3
# coding=utf-8

import ProcesadorTablaDisponibles, sys

procesador=ProcesadorTablaDisponibles("..", "gestion.settings", sys.argv[1])

procesador.procesar_tabla()