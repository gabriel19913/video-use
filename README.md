# Atualização da Skill Video-Use: Transição para Whisper-Docker

Este documento descreve detalhadamente as mudanças implementadas na skill `video-use` e demonstra como seu funcionamento atual difere da sua versão anterior.

---

## 🕰️ Como funcionava anteriormente

1. **Transcrição Paga (Nuvem):**  
   A skill dependia da API ElevenLabs Scribe para gerar a transcrição e separar os tempos de cada palavra. Isso exigia a configuração obrigatória de uma `ELEVENLABS_API_KEY`, gerando custos por uso, necessidade de internet constante, tempo de upload dos arquivos de áudio para servidores de terceiros e limitações de privacidade.
2. **Formato Legado do JSON:**  
   O formato de transcrição retornava uma estrutura contendo `words` e marcações de tempo (incluindo "spacings"), que alimentava o gerador de takes (arquivo compactado lido pela IA).
3. **Foco Mais Genérico na Edição:**  
   Embora o agente conseguisse editar o vídeo a partir do texto, ele possuía uma abordagem mais generalizada na escolha dos cortes, carecendo de um mandato claro e rígido sobre o que priorizar durante uma "limpeza" de rotina do material bruto.

---

## 🚀 Como funciona agora

1. **Transcrição Local via Docker (Gratuita, Privada e Ilimitada):**  
   A dependência de APIs externas foi totalmente removida. O script `helpers/transcribe.py` foi reescrito para utilizar o ecossistema do **`whisper-docker`**.
   - A transcrição agora roda via `docker compose` em contêineres locais.
   - É utilizado por padrão o modelo `turbo` do OpenAI Whisper.
   - **Vantagem:** Privacidade total, sem custos por requisição, altíssima agilidade (especialmente quando houver GPU disponível) e sem limites de tamanho de áudio.

2. **Compatibilidade Flexível no Empacotamento de Texto:**  
   O arquivo `helpers/pack_transcripts.py` foi reescrito para analisar os arquivos `.json` nativos do Whisper (em que a hierarquia divide `segments` e dentro deles, `words`).
   - A skill continua gerando as quebras automáticas em silêncios prolongados, unindo as pontas de forma transparente e mantendo total compatibilidade retroativa se você ainda possuir projetos antigos.

3. **Subagente Implacável contra Retakes e Silêncios (O "Assistente de Limpeza"):**  
   As instruções primárias da skill (`SKILL.md`) foram significativamente aprimoradas para definir um norte cristalino ao agente:
   - **Eliminação de Duplicidades:** Ao analisar frases transcritas, o agente agora é ativamente instruído a procurar por repetições e engasgos. Diante de múltiplas tentativas na mesma fala (retakes), ele deve sempre amputar o erro e manter apenas **o último take limpo**.
   - **Tolerância Zero para "Dead Air":** Os silêncios acima de um limite se tornaram automaticamente alvos de corte para dar dinamismo extremo ao material gravado.

---

## 🎯 Diferenciais na Prática

Ao utilizar a skill no fluxo moderno, a mágica acontece de forma muito mais coesa para o usuário. Basta:

1. Jogar seus clipes brutos (formato `.mp4`) dentro da sua pasta de projeto.
2. Pedir ao agente para "Fazer a edição".
3. **Resultado:** O áudio nem sai do seu computador. O Whisper processa o texto internamente através do Docker; o LLM interpreta as falas de forma textual; caça todas as suas gaguejadas, retakes e momentos onde você parou para pensar; aplica crossfades precisos para esconder os cortes, avalia visualmente se os cortes fizeram sentido, e exporta no final um `final.mp4` **fluido, magistralmente editado e com timing impecável**. Tudo isso respeitando restrições estritas de produção de vídeo profissional.
