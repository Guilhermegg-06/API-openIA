import os
from typing import Dict

from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def carregar_configuracao() -> Dict:
    load_dotenv() 
    api_key = os.getenv("OPENAI_API_KEY")
    tem_chave = api_key is not None and api_key.strip() != ""

    return {
        "api_key": api_key,
        "tem_chave": tem_chave,
    }


def coletar_dados_usuario() -> Dict:
    print("<<<<<<< Organizador de Estudos OpenIA >>>>>>>>\n")

    assunto = input("Qual é o assunto que você quer estudar? ")
    objetivo = input(
        "Qual é o seu objetivo com esse estudo? (ex: prova X, concurso, aprender do zero) "
    )

    # semanas de estudo
    while True:
        try:
            semanas = int(input("Por quantas semanas você quer estudar? "))
            if semanas <= 0:
                raise ValueError
            break
        except ValueError:
            print("Por favor, digite um número inteiro positivo para semanas.\n")

    # horas por dia
    while True:
        try:
            horas_por_dia = float(
                input("Quantas horas por dia você consegue estudar? (ex: 1.5) ")
            )
            if horas_por_dia <= 0:
                raise ValueError
            break
        except ValueError:
            print("Por favor, digite um número válido para horas (ex: 1, 1.5, 2).\n")

    print("\nNível atual no assunto:")
    print("1 - Iniciante")
    print("2 - Intermediário")
    print("3 - Avançado")

    nivel_map = {1: "iniciante", 2: "intermediário", 3: "avançado"}

    while True:
        try:
            nivel_opcao = int(input("Escolha o nível (1, 2 ou 3): "))
            if nivel_opcao not in nivel_map:
                raise ValueError
            nivel = nivel_map[nivel_opcao]
            break
        except ValueError:
            print("Opção inválida. Digite 1, 2 ou 3.\n")

    print("\nEstilo preferido de estudo:")
    print("1 - Mais teoria")
    print("2 - Mais prática")
    print("3 - Misto")

    estilo_map = {1: "mais teoria", 2: "mais prática", 3: "misto"}

    while True:
        try:
            estilo_opcao = int(input("Escolha o estilo (1, 2 ou 3): "))
            if estilo_opcao not in estilo_map:
                raise ValueError
            estilo = estilo_map[estilo_opcao]
            break
        except ValueError:
            print("Opção inválida. Digite 1, 2 ou 3.\n")

    print("\nValeu! Vou montar o seu plano de estudos...\n")

    return {
        "assunto": assunto,
        "objetivo": objetivo,
        "semanas": semanas,
        "horas_por_dia": horas_por_dia,
        "nivel": nivel,
        "estilo": estilo,
    }


def gerar_plano_com_ia(dados: Dict) -> str:

    if OpenAI is None:
        raise RuntimeError(
            "Biblioteca 'openai' não está instalada. Rode 'pip install -r requirements.txt'."
        )

   
    client = OpenAI()

    prompt = f"""
Você é um organizador de estudos especializado em ajudar estudantes a montar rotinas realistas.

Com base nos dados abaixo, crie um plano de estudos organizado por semanas e dias.

DADOS DO ESTUDANTE
- Assunto principal: {dados['assunto']}
- Objetivo: {dados['objetivo']}
- Duração: {dados['semanas']} semana(s)
- Horas disponíveis por dia: {dados['horas_por_dia']}
- Nível atual: {dados['nivel']}
- Estilo preferido: {dados['estilo']}

INSTRUÇÕES DE FORMATO
1. Comece com um pequeno resumo em 3 tópicos.
2. Depois, descreva o plano semana a semana, usando este formato textual:
   Semana 1:
     - Dia 1: ...
     - Dia 2: ...
   Semana 2:
     - ...
3. No final, inclua 3 dicas rápidas para manter a disciplina.
4. Use uma linguagem em português brasileiro, simples e motivadora.
5. Use no máximo aproximadamente 600 palavras.
"""

    response = client.responses.create(
        model="gpt-5-nano", 
        input=prompt,
    )

    plano_texto = response.output_text  

    return "=== PLANO DE ESTUDOS (GERADO COM IA) ===\n\n" + plano_texto


def main() -> None:
    config = carregar_configuracao()
    dados = coletar_dados_usuario()

    if config["tem_chave"]:
        print("Chave de API encontrada. Tentando gerar plano com IA...\n")
        try:
            plano = gerar_plano_com_ia(dados)
        except Exception as exc:
            print("Ocorreu um erro ao chamar a API de IA:")
            print(f"  {exc}\n")
            # fallback simples, sem IA, só pra não quebrar o programa
            plano = (
                "Não foi possível usar a IA agora.\n"
                "Dica: divida o conteúdo que você precisa estudar em "
                f"{dados['semanas']} parte(s) e separe as {dados['horas_por_dia']}h por dia\n"
                "entre revisão, conteúdo novo e exercícios.\n"
            )
    else:
        print("Nenhuma chave de API foi encontrada.\n")
        plano = (
            "Para gerar um plano detalhado com IA, configure a variável OPENAI_API_KEY\n"
            "no arquivo .env.\n\n"
            "Enquanto isso, você pode organizar seu estudo dividindo o assunto "
            f"'{dados['assunto']}' em tópicos semanais e usando as horas por dia\n"
            "para revisar, ver conteúdo novo e praticar exercícios.\n"
        )

    print(plano)


if __name__ == "__main__":
    main()
