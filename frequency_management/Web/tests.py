from io import BytesIO
from django.test import TestCase
from web.views import gerar_relatorio_pdf
from django.test import TestCase


# GERAR RELATÓRIO
class GerarRelatorioPdfTestCase(TestCase):

     def test_geracao_pdf(self):
         # Mock dos dados para o relatório
         relatorio = [
             {"categoria": "Top Atrasos", "nome": "João Silva", "turma": "DS101", "total_atrasos": 5, "total_faltas": 2},
             {"categoria": "Baixa Frequência", "nome": "Maria Souza", "turma": "DS102", "total_atrasos": 3, "total_faltas": 10},
         ]

         pdf_buffer = gerar_relatorio_pdf(relatorio)

         # Validações
         self.assertIsInstance(pdf_buffer, BytesIO)  # Certifica-se de que o retorno é um BytesIO
         self.assertGreater(len(pdf_buffer.getvalue()), 0)  # Verifica se o PDF não está vazio

