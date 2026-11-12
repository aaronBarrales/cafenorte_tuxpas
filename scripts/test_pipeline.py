"""Pruebas de límites de negocio con datos sintéticos sin información personal."""
import unittest

import pandas as pd

from pipeline import attach_cost, cents, monthly, parse_days, rotation, stockouts, unique


class PipelineTests(unittest.TestCase):
    def test_fecha_nula_se_rechaza(self):
        with self.assertRaises(ValueError):
            parse_days(pd.Series(['2026-01-01', None]))

    def test_stock_desconocido_interrumpe_racha(self):
        s = pd.DataFrame({'dia': pd.date_range('2026-01-01', periods=5), 'tienda_id': 'T', 'sku_erp': 'A', 'stock_num': [0, 0, None, 0, 0]})
        self.assertTrue(stockouts(s, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-01-31')).empty)

    def test_rotacion_denominador_cero(self):
        s = pd.DataFrame({'dia': pd.to_datetime(['2026-01-01']), 'tienda_id': 'T', 'sku_erp': 'A', 'stock_num': 0})
        v = pd.DataFrame({'dia': pd.to_datetime(['2026-01-01']), 'tienda_id': 'T', 'sku_erp': 'A', 'cantidad': 1, 'tipo_comprobante': 'I'})
        self.assertTrue(pd.isna(rotation(v, s, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-01-01')).rotacion_veces.iloc[0]))

    def test_mom_base_cero(self):
        f = pd.DataFrame({'dia': pd.to_datetime(['2025-12-01', '2026-01-01']), 'canal': 'fisico', 'ingreso_centavos': [0, 100], 'fila_id': [0, 1]})
        r = monthly(f, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-01-31'))
        self.assertTrue(r[r.canal.eq('fisico')].crecimiento_pct.isna().all())

    def test_redondeo_financiero(self):
        self.assertEqual(cents('1.005'), 101)
        self.assertEqual(cents('10', '17.1234'), 17123)

    def test_costos_vigentes_sin_futuro(self):
        f = pd.DataFrame({'sku_erp': ['A', 'A', 'A', None], 'dia': pd.to_datetime(['2026-01-01', '2026-01-10', '2025-12-01', '2026-01-01']), 'fila_id': range(4)})
        c = pd.DataFrame({'sku_erp': ['A', 'A'], 'vigencia': pd.to_datetime(['2026-01-01', '2026-01-10']), 'costo_mxn': [10, 20]})
        r = attach_cost(f, c)
        self.assertEqual(r.costo_mxn.iloc[:2].tolist(), [10, 20])
        self.assertTrue(r.costo_mxn.iloc[2:].isna().all())

    def test_clave_duplicada_se_rechaza(self):
        with self.assertRaises(ValueError):
            unique(pd.DataFrame({'sku': ['A', 'A']}), ['sku'])

    def test_quiebres_tres_cuatro_y_huecos(self):
        dates = ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-05', '2026-01-06', '2026-01-07', '2026-01-08']
        s = pd.DataFrame({'dia': pd.to_datetime(dates), 'tienda_id': 'T', 'sku_erp': 'A', 'stock_num': 0})
        r = stockouts(s, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-03-31'))
        self.assertEqual(r.dias.tolist(), [4])
        self.assertEqual(r.inicio.iloc[0], pd.Timestamp('2026-01-05'))

    def test_rotacion_poblacion_compatible(self):
        s = pd.DataFrame({'dia': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-01']), 'tienda_id': ['T', 'T', 'X'], 'sku_erp': 'A', 'stock_num': [10, 30, 100]})
        v = pd.DataFrame({'dia': pd.to_datetime(['2026-01-01'] * 3), 'tienda_id': ['T', 'X', 'T'], 'sku_erp': 'A', 'cantidad': [40, 999, 10], 'tipo_comprobante': ['I', 'I', 'E']})
        r = rotation(v, s, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-01-02'))
        self.assertEqual(r.rotacion_veces.iloc[0], 2)
        self.assertEqual(r.tiendas.iloc[0], 1)

    def test_mom_no_salta_mes_ausente_ni_divide_cero(self):
        f = pd.DataFrame({'dia': pd.to_datetime(['2025-12-01', '2026-01-01', '2026-03-01']), 'canal': 'fisico', 'ingreso_centavos': [10000, 12000, 15000], 'fila_id': range(3)})
        r = monthly(f, pd.Timestamp('2026-01-01'), pd.Timestamp('2026-03-31'))
        physical = r[r.canal.eq('fisico')]
        self.assertAlmostEqual(physical.crecimiento_pct.iloc[0], 20)
        self.assertTrue(pd.isna(physical.crecimiento_pct.iloc[2]))


if __name__ == '__main__':
    unittest.main()
