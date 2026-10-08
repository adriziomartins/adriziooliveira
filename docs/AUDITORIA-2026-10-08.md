# Auditoria técnica do acervo — 2026-10-08

## Escopo
Inspeção da árvore da branch `main`, referências de navegação nas páginas principais e referências `img src` nas 11 fichas individuais existentes. Não é teste de renderização em navegador nem confirmação HTTP das imagens externas.

## Constatações
- GitHub Pages configurado para `main` / `(root)`; usuário confirmou visualização do site.
- Arquivos HTML, CSS, JavaScript e `.nojekyll` estão no repositório.
- **Não existe `assets/img/acervo/` na árvore publicada.**
- Quatro fichas apontam para imagens locais inexistentes:
  - `registros/ao-foto-010.html` → `../assets/img/acervo/ao-foto-010.jpg`
  - `registros/ao-foto-012.html` → `../assets/img/acervo/ao-foto-012.jpg`
  - `registros/ao-foto-013.html` → `../assets/img/acervo/ao-foto-013.jpg`
  - `registros/ao-foto-014.html` → `../assets/img/acervo/ao-foto-014.jpg`
- As outras sete fichas consultadas usam URLs externas do blog `adrizio.home.blog`. A disponibilidade HTTP dessas URLs não foi verificada.
- `organizacoes/relacionamentos.html` existe e `organizacoes/index.html` contém link para essa matriz.
- A árvore contém fichas AO-FOTO-003, 005, 006, 008–014 e AO-DOC-001–002. Não contém fichas AO-FOTO-001, 002, 004 e 007. Isso não significa necessariamente que sejam necessárias páginas separadas, mas a lacuna deve ser decidida editorialmente.

## Prioridades
1. Recuperar os quatro arquivos originais, confirmar proveniência e só então publicá-los na pasta `assets/img/acervo/`; alternativamente apontar as fichas para URLs originais verificadas.
2. Verificar HTTP 200, tipo de mídia, autoria, atribuição e direitos de reprodução de todas as imagens externas.
3. Auditar sistematicamente todos os `href` relativos, âncoras e menus em todas as páginas.
4. Conferir a consistência dos identificadores, datas e níveis V0–V2 entre fichas, cronologia, fontes e matriz.
5. Executar testes de responsividade e acessibilidade em navegador.

## Regra editorial
Não atribuir data, cargo, organização, autoria ou identidade de arquivo apenas por nome de imagem. Não substituir imagem histórica por fotografia ilustrativa. Registrar a origem e o estado de verificação antes de publicar.
