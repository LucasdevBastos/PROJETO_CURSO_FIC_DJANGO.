# Avatares Padrão

Esta pasta deve conter os 7 avatares padrão do sistema.

## Arquivos necessários:

- `avatar_1.jpg`
- `avatar_2.jpg`
- `avatar_3.jpg`
- `avatar_4.jpg`
- `avatar_5.jpg`
- `avatar_6.jpg`
- `avatar_7.jpg`

## Instruções:

1. Coloque suas 7 imagens JPG nesta pasta com os nomes exatos acima
2. Recomendação de tamanho: 200x200px ou 300x300px (quadradas)
3. Formato: JPG (mas o sistema pode ser facilmente adaptado para PNG se necessário)

## Como os avatares são usados:

- Qualquer usuário pode escolher qualquer um dos 7 avatares
- Os avatares são exibidos usando o método `get_avatar_url()` do modelo Perfil
- O caminho usado será: `/static/avatars/avatar_X.jpg`

## Sistema VIP:

- Apenas usuários VIP podem ter avatares e banners personalizados
- Para usuários não-VIP, apenas os avatares padrão estão disponíveis
