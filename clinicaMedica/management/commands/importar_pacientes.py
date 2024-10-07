import json
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from clinicaMedica.models import Paciente
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa pacientes de um arquivo JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Caminho para o arquivo JSON')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        self.stdout.write(self.style.SUCCESS(f'Tentando abrir o arquivo: {json_file}'))
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                pacientes_data = json.load(file)
            self.stdout.write(self.style.SUCCESS(f'Arquivo JSON lido com sucesso. Encontrados {len(pacientes_data)} registros.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo JSON: {str(e)}'))
            return

        if not isinstance(pacientes_data, list):
            self.stdout.write(self.style.ERROR('O JSON não contém uma lista de pacientes.'))
            return

        pacientes_importados = 0
        for index, paciente_data in enumerate(pacientes_data, start=1):
            self.stdout.write(f'Processando paciente {index} de {len(pacientes_data)}')
            try:
                # Verifica se todos os campos necessários estão presentes
                campos_obrigatorios = ['cpf', 'nome', 'email', 'celular', 'endereco', 'data_nasc', 'estado', 'cep', 'sexo']
                for campo in campos_obrigatorios:
                    if campo not in paciente_data:
                        raise KeyError(f'Campo obrigatório {campo} não encontrado')


                estado = paciente_data['cidade'] + ", " + paciente_data['estado']

                # Converte a string de data para um objeto date
                data_nascimento = datetime.strptime(paciente_data['data_nasc'], '%d/%m/%Y').date()
                data_nascimento_str = paciente_data['data_nasc']

                paciente = Paciente(
                    cpf=paciente_data['cpf'],
                    nome=paciente_data['nome'],
                    email=paciente_data['email'],
                    telefone=paciente_data['celular'],
                    endereco=paciente_data['endereco'],
                    data_de_nascimento=data_nascimento,
                    sexo=paciente_data['sexo'],
                    estado=estado,
                    cep=paciente_data['cep']
                )
                paciente.save()
                pacientes_importados += 1
                self.stdout.write(self.style.SUCCESS(f'Paciente {paciente.nome} importado com sucesso'))
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(f'Erro de integridade ao importar paciente: {str(e)}'))
            except KeyError as e:
                self.stdout.write(self.style.ERROR(f'Erro nos dados do paciente: {str(e)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao importar paciente: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Importação concluída. {pacientes_importados} pacientes importados com sucesso.'))