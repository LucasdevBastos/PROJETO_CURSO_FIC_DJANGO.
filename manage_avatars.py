"""
Script de gerenciamento de perfis e sistema VIP

Execute com:
python manage.py shell < manage_avatars.py

Ou use interativamente no shell:
python manage.py shell
>>> exec(open('manage_avatars.py').read())
"""

from django.contrib.auth.models import User
from perfil.models import Perfil


def criar_perfis_faltantes():
    """
    Cria perfis para todos os usuários que ainda não têm um
    """
    usuarios_sem_perfil = User.objects.filter(perfil__isnull=True)
    criados = 0
    
    for usuario in usuarios_sem_perfil:
        Perfil.objects.create(user=usuario)
        criados += 1
        print(f"✅ Perfil criado para: {usuario.username}")
    
    if criados == 0:
        print("ℹ️  Todos os usuários já têm perfil!")
    else:
        print(f"\n✨ Total de perfis criados: {criados}")
    
    return criados


def tornar_vip(username):
    """
    Torna um usuário VIP pelo username
    
    Uso:
    >>> tornar_vip('joao')
    """
    try:
        perfil = Perfil.objects.get(user__username=username)
        perfil.is_vip = True
        perfil.save()
        print(f"💎 {username} agora é VIP!")
        return True
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")
        return False


def remover_vip(username):
    """
    Remove status VIP de um usuário
    Automaticamente limpa custom_avatar e custom_banner
    
    Uso:
    >>> remover_vip('joao')
    """
    try:
        perfil = Perfil.objects.get(user__username=username)
        perfil.is_vip = False
        perfil.save()  # O método save() do modelo vai limpar os campos personalizados
        print(f"ℹ️  {username} não é mais VIP")
        print(f"   Avatar personalizado e banner foram removidos automaticamente")
        return True
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")
        return False


def listar_vips():
    """
    Lista todos os usuários VIP
    
    Uso:
    >>> listar_vips()
    """
    vips = Perfil.objects.filter(is_vip=True).select_related('user')
    
    if not vips.exists():
        print("ℹ️  Nenhum usuário VIP encontrado")
        return
    
    print(f"\n💎 Usuários VIP ({vips.count()}):\n")
    print(f"{'Username':<20} {'Avatar':<20} {'Custom Avatar':<15} {'Custom Banner':<15}")
    print("-" * 70)
    
    for perfil in vips:
        custom_avatar_status = "✅" if perfil.custom_avatar else "❌"
        custom_banner_status = "✅" if perfil.custom_banner else "❌"
        
        print(f"{perfil.user.username:<20} {perfil.avatar_choice:<20} {custom_avatar_status:<15} {custom_banner_status:<15}")


def definir_avatar_padrao(username, avatar_numero):
    """
    Define o avatar padrão de um usuário (1-7)
    
    Uso:
    >>> definir_avatar_padrao('joao', 3)  # Define avatar_3.jpg
    """
    if not 1 <= avatar_numero <= 7:
        print("❌ Número do avatar deve ser entre 1 e 7")
        return False
    
    try:
        perfil = Perfil.objects.get(user__username=username)
        perfil.avatar_choice = f'avatar_{avatar_numero}.jpg'
        perfil.save()
        print(f"✅ Avatar de {username} alterado para avatar_{avatar_numero}.jpg")
        return True
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")
        return False


def definir_avatar_personalizado(username, url):
    """
    Define avatar personalizado para um usuário VIP
    
    Uso:
    >>> definir_avatar_personalizado('joao', 'https://exemplo.com/avatar.jpg')
    """
    try:
        perfil = Perfil.objects.get(user__username=username)
        
        if not perfil.is_vip:
            print(f"❌ {username} não é VIP! Torne o usuário VIP primeiro.")
            print(f"   Use: tornar_vip('{username}')")
            return False
        
        perfil.custom_avatar = url
        perfil.save()
        print(f"✅ Avatar personalizado definido para {username}")
        print(f"   URL: {url}")
        return True
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")
        return False


def definir_banner_personalizado(username, url):
    """
    Define banner personalizado para um usuário VIP
    
    Uso:
    >>> definir_banner_personalizado('joao', 'https://exemplo.com/banner.jpg')
    """
    try:
        perfil = Perfil.objects.get(user__username=username)
        
        if not perfil.is_vip:
            print(f"❌ {username} não é VIP! Torne o usuário VIP primeiro.")
            print(f"   Use: tornar_vip('{username}')")
            return False
        
        perfil.custom_banner = url
        perfil.save()
        print(f"✅ Banner personalizado definido para {username}")
        print(f"   URL: {url}")
        return True
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")
        return False


def estatisticas_avatares():
    """
    Mostra estatísticas sobre o uso de avatares
    
    Uso:
    >>> estatisticas_avatares()
    """
    total_perfis = Perfil.objects.count()
    total_vips = Perfil.objects.filter(is_vip=True).count()
    total_com_custom_avatar = Perfil.objects.filter(custom_avatar__isnull=False).exclude(custom_avatar='').count()
    total_com_custom_banner = Perfil.objects.filter(custom_banner__isnull=False).exclude(custom_banner='').count()
    
    print("\n📊 Estatísticas de Avatares")
    print("=" * 50)
    print(f"Total de perfis: {total_perfis}")
    print(f"Usuários VIP: {total_vips} ({total_vips/total_perfis*100:.1f}%)" if total_perfis > 0 else "Usuários VIP: 0")
    print(f"Com avatar personalizado: {total_com_custom_avatar}")
    print(f"Com banner personalizado: {total_com_custom_banner}")
    print()
    
    # Distribuição de avatares padrão
    print("Distribuição de avatares padrão:")
    for i in range(1, 8):
        avatar_file = f'avatar_{i}.jpg'
        count = Perfil.objects.filter(avatar_choice=avatar_file).count()
        barra = "█" * int(count / total_perfis * 50) if total_perfis > 0 else ""
        print(f"  Avatar {i}: {count:3d} {barra}")


def info_usuario(username):
    """
    Mostra informações completas do perfil de um usuário
    
    Uso:
    >>> info_usuario('joao')
    """
    try:
        perfil = Perfil.objects.get(user__username=username)
        usuario = perfil.user
        
        print(f"\n👤 Informações de {username}")
        print("=" * 50)
        print(f"Nome completo: {usuario.first_name} {usuario.last_name}".strip() or "Não definido")
        print(f"Email: {usuario.email}")
        print(f"Data de cadastro: {usuario.date_joined.strftime('%d/%m/%Y')}")
        print(f"\nStatus VIP: {'💎 Sim' if perfil.is_vip else '❌ Não'}")
        print(f"Avatar padrão: {perfil.avatar_choice}")
        print(f"Avatar personalizado: {perfil.custom_avatar or 'Não definido'}")
        print(f"Banner personalizado: {perfil.custom_banner or 'Não definido'}")
        print(f"\nURL do avatar: {perfil.get_avatar_url()}")
        
        if perfil.bio:
            print(f"\nBio: {perfil.bio}")
        
        print(f"\nPerfil criado: {perfil.criado_em.strftime('%d/%m/%Y %H:%M')}")
        print(f"Última atualização: {perfil.atualizado_em.strftime('%d/%m/%Y %H:%M')}")
        
    except Perfil.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado ou não tem perfil")


def tornar_todos_vip():
    """
    Torna TODOS os usuários VIP (usar com cuidado!)
    
    Uso:
    >>> tornar_todos_vip()
    """
    resposta = input("⚠️  Tem certeza que quer tornar TODOS os usuários VIP? (s/n): ")
    
    if resposta.lower() != 's':
        print("Operação cancelada")
        return False
    
    perfis = Perfil.objects.all()
    perfis.update(is_vip=True)
    
    print(f"✅ {perfis.count()} usuários agora são VIP!")
    return True


def remover_todos_vip():
    """
    Remove status VIP de TODOS os usuários (usar com cuidado!)
    
    Uso:
    >>> remover_todos_vip()
    """
    resposta = input("⚠️  Tem certeza que quer remover status VIP de TODOS? (s/n): ")
    
    if resposta.lower() != 's':
        print("Operação cancelada")
        return False
    
    perfis = Perfil.objects.filter(is_vip=True)
    count = perfis.count()
    
    for perfil in perfis:
        perfil.is_vip = False
        perfil.save()  # Usa o método save() para limpar campos personalizados
    
    print(f"✅ Status VIP removido de {count} usuários")
    print(f"   Avatares e banners personalizados foram limpos automaticamente")
    return True


def menu_interativo():
    """
    Menu interativo para gerenciamento de avatares
    
    Uso:
    >>> menu_interativo()
    """
    while True:
        print("\n" + "="*50)
        print("🎨 GERENCIAMENTO DE AVATARES E VIP")
        print("="*50)
        print("1. Criar perfis faltantes")
        print("2. Tornar usuário VIP")
        print("3. Remover VIP de usuário")
        print("4. Listar todos os VIPs")
        print("5. Definir avatar padrão")
        print("6. Definir avatar personalizado (VIP)")
        print("7. Definir banner personalizado (VIP)")
        print("8. Ver estatísticas")
        print("9. Ver informações de usuário")
        print("0. Sair")
        print()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            criar_perfis_faltantes()
        
        elif opcao == '2':
            username = input("Username: ").strip()
            tornar_vip(username)
        
        elif opcao == '3':
            username = input("Username: ").strip()
            remover_vip(username)
        
        elif opcao == '4':
            listar_vips()
        
        elif opcao == '5':
            username = input("Username: ").strip()
            avatar_numero = int(input("Número do avatar (1-7): ").strip())
            definir_avatar_padrao(username, avatar_numero)
        
        elif opcao == '6':
            username = input("Username: ").strip()
            url = input("URL do avatar: ").strip()
            definir_avatar_personalizado(username, url)
        
        elif opcao == '7':
            username = input("Username: ").strip()
            url = input("URL do banner: ").strip()
            definir_banner_personalizado(username, url)
        
        elif opcao == '8':
            estatisticas_avatares()
        
        elif opcao == '9':
            username = input("Username: ").strip()
            info_usuario(username)
        
        elif opcao == '0':
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")


# Ajuda
def ajuda():
    """
    Mostra todas as funções disponíveis
    """
    print("\n📚 FUNÇÕES DISPONÍVEIS:")
    print("=" * 70)
    print("criar_perfis_faltantes()          - Cria perfis para usuários sem perfil")
    print("tornar_vip('username')            - Torna um usuário VIP")
    print("remover_vip('username')           - Remove status VIP")
    print("listar_vips()                     - Lista todos os VIPs")
    print("definir_avatar_padrao('user', 3)  - Define avatar padrão (1-7)")
    print("definir_avatar_personalizado(...) - Define avatar custom (VIP)")
    print("definir_banner_personalizado(...) - Define banner custom (VIP)")
    print("estatisticas_avatares()           - Mostra estatísticas")
    print("info_usuario('username')          - Info completa de um usuário")
    print("menu_interativo()                 - Menu interativo")
    print("ajuda()                           - Mostra esta ajuda")
    print("=" * 70)


# Executar automaticamente ao carregar
print("\n🎨 Sistema de Gerenciamento de Avatares carregado!")
print("Digite: ajuda() para ver todas as funções disponíveis")
print("Digite: menu_interativo() para usar o menu interativo")
print()
