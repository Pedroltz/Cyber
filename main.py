import os
import sys
import time
import random
import ipaddress
import pygame
import keyboard
from typing import List, Dict, Optional
from colorama import init, Fore, Back, Style
from dataclasses import dataclass


# Inicializa o mixer do pygame para áudio
pygame.mixer.init()

CYBER_LOGO = """
█░█ █▀▀ █▄▀ ▀█▀ █▀█ █▀█   █▀█ █▀
▀▄▀ ██▄ █░█ ░█░ █▄█ █▀▄   █▄█ ▄█  v2.1.0
"""

COMING_SOON_ART = """
╔══════════════════════════════════════════════╗
║       ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ╔═╗╔═╗╔═╗╔╗╔         ║
║       ║  ║ ║║║║║║║║║ ╦  ╚═╗║ ║║ ║║║║         ║
║       ╚═╝╚═╝╩ ╩╩╝╚╝╚═╝  ╚═╝╚═╝╚═╝╝╚╝         ║
║                                              ║
║        [DISPONÍVEL NA VERSÃO v2.2.0]         ║
║     [AGUARDE AS PRÓXIMAS ATUALIZAÇÕES]       ║
╚══════════════════════════════════════════════╝
"""

@dataclass
class HackType:
    code: str
    name: str
    coming_soon: bool = False

HACK_TYPES = [
    HackType("DAEMON_BREACH", "Quebra de Daemon Neural"),
    HackType("NEURAL_BYPASS", "Bypass Neural [v2.2.0]", True),
    HackType("DARKNET_DIVE", "Mergulho na Darknet [v2.2.0]", True),
    HackType("QUANTUM_CRACK", "Decodificador Quântico")
]

class SoundManager:
    def __init__(self, volume: float = 0.3):
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self.volume = volume
        self._load_sounds()

    def _load_sounds(self):
        sound_files = {
            'type': 'sounds/type.mp3',
            'select': 'sounds/select.mp3',
            'move': 'sounds/move.mp3',
            'success': 'sounds/success.mp3',
            'failure': 'sounds/failure.mp3',
            'alert': 'sounds/alert.mp3',
            'startup': 'sounds/startup.mp3',
            'scanning': 'sounds/scanning.mp3',
            'shutdown': 'sounds/shutdown.mp3'
        }
        
        try:
            for name, path in sound_files.items():
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
        except:
            print(Fore.RED + "[ERRO] Arquivos de som não encontrados! Continuando sem sons...")
            time.sleep(2)
            self.sounds = {}

    def play(self, sound_name: str, loop: int = 0):
        if sound := self.sounds.get(sound_name):
            try:
                sound.play(loops=loop)
            except:
                pass

    def stop(self, sound_name: str):
        if sound := self.sounds.get(sound_name):
            try:
                sound.stop()
            except:
                pass

class MenuManager:
    @staticmethod
    def wait_key():
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name
        return None

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_menu(options: List[str], selected: int):
        for i, option in enumerate(options):
            if i == selected:
                print(Fore.GREEN + "► " + option + " ◄" + Style.RESET_ALL)
            else:
                print(Fore.CYAN + "  " + option + "  " + Style.RESET_ALL)

    def menu_selection(self, options: List[str], header: str = "SELECIONE UMA OPÇÃO", sound_manager: Optional[SoundManager] = None) -> int:
        selected = 0
        while True:
            self.clear_screen()
            print(Fore.GREEN + CYBER_LOGO)
            print(Fore.CYAN + "="*60)
            print(Fore.GREEN + header.center(60))
            print(Fore.CYAN + "="*60 + "\n")
            
            self.print_menu(options, selected)
            print("\n" + Fore.YELLOW + "[USE ↑↓ PARA NAVEGAR E ENTER PARA SELECIONAR]" + Style.RESET_ALL)

            key = self.wait_key()
            if key == 'up' and selected > 0:
                selected -= 1
                if sound_manager:
                    sound_manager.play('move')
            elif key == 'down' and selected < len(options) - 1:
                selected += 1
                if sound_manager:
                    sound_manager.play('move')
            elif key == 'enter':
                if sound_manager:
                    sound_manager.play('select')
                return selected
class CyberTerminal:
    def __init__(self):
        init(autoreset=True)
        self.running = True
        self.current_hack = None
        self.sound_manager = SoundManager()
        self.menu_manager = MenuManager()

    def print_fast(self, text: str, color=Fore.CYAN, delay: float = 0.001, sound: bool = True):
        for char in text:
            if sound and char not in [' ', '\n']:
                self.sound_manager.play('type')
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)

    def display_coming_soon(self) -> bool:
        self.menu_manager.clear_screen()
        self.sound_manager.play('failure')
        print(Fore.YELLOW + COMING_SOON_ART)
        print(Fore.YELLOW + "[PRESSIONE ENTER PARA VOLTAR]")
        input()
        return False

    def startup_sequence(self):
        self.menu_manager.clear_screen()
        self.sound_manager.play('startup')
        
        startup_text = [
            "[INICIANDO VEKTOR_OS 2077]",
            "[CARREGANDO DRIVERS NEURAIS...]",
            "[INTERFACE BIOMECÂNICA ONLINE]",
            "[CONECTANDO À MATRIX GLOBAL...]",
            "[BYPASSANDO PROTOCOLOS ICE...]",
            "[PROTOCOLOS DE SEGURANÇA ATIVOS]",
            "[BEM-VINDO À MATRIX, RUNNER]"
        ]
        
        for line in CYBER_LOGO.split('\n'):
            self.print_fast(line, Fore.GREEN, delay=0.1)
            
        for text in startup_text:
            self.print_fast(text)
            time.sleep(0.2)
        
        time.sleep(0.5)
        self.menu_manager.clear_screen()

    def main_menu(self) -> int:
        options = [
            "Iniciar Exploit",
            "Desconectar do SO"
        ]
        return self.menu_manager.menu_selection(options, "THE ULTIMATE NEURAL HACKING TOOL", self.sound_manager)

    def select_hack_type(self) -> bool:
        options = [hack.name for hack in HACK_TYPES]
        selected = self.menu_manager.menu_selection(options, "SELECIONE O EXPLOIT", self.sound_manager)
        self.current_hack = HACK_TYPES[selected]
        
        if self.current_hack.coming_soon:
            return self.display_coming_soon()
        return True

    @staticmethod
    def roll_dice(num_dice: int) -> List[int]:
        return [random.randint(1, 6) for _ in range(num_dice)]

    @staticmethod
    def generate_random_ip() -> str:
        return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

    @staticmethod
    def generate_security_code() -> str:
        chars = "0123456789ABCDEF"
        return "-".join(
            "".join(random.choice(chars) for _ in range(4))
            for _ in range(3)
        )

    def display_rolling_animation(self, final_rolls: List[int]):
        loading_chars = ["■", "□"]
        bar_size = 30
        
        def create_loading_bar(progress: float) -> str:
            filled = int(bar_size * progress)
            bar = "".join(loading_chars[0] if i < filled else loading_chars[1] for i in range(bar_size))
            return f"[{bar}] {int(progress * 100)}%"

        self.sound_manager.play('scanning', -1)

        try:
            steps = 30
            for i in range(steps + 1):
                progress = i / steps
                self.menu_manager.clear_screen()
                print(Fore.GREEN + f"[EXECUTANDO {self.current_hack.name}]")
                print(Fore.CYAN + create_loading_bar(progress))
                print(Fore.YELLOW + "\n[INICIALIZANDO MÓDULOS DE INTRUSÃO]")
                time.sleep(0.1)
            
            self.sound_manager.stop('scanning')
            
            for _ in range(3):
                for color in [Fore.RED, Fore.CYAN]:
                    self.menu_manager.clear_screen()
                    print(Fore.GREEN + f"[EXECUTANDO {self.current_hack.name}]")
                    print(color + create_loading_bar(1.0))
                    print(Fore.YELLOW + "\n[PROCESSANDO DADOS...]")
                    time.sleep(0.1)

            self.menu_manager.clear_screen()
            print(Fore.GREEN + f"[EXECUTANDO {self.current_hack.name}]")
            print(Fore.GREEN + create_loading_bar(1.0))
            print(Fore.YELLOW + f"\n[RESULTADO DA INTRUSÃO]: {final_rolls}")
            time.sleep(1)
            print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
            input()
            
        except Exception as e:
            self.sound_manager.stop('scanning')
            raise e

    def simulate_hack_attempt(self):
        if not self.select_hack_type():
            return
        
        self.menu_manager.clear_screen()
        self.print_fast(f"[INICIANDO {self.current_hack.name}]", Fore.GREEN)
        print(Fore.CYAN + "[DIGITE NÚMERO DE MÓDULOS DE INTRUSÃO (1-10)] >>> ", end="")
        
        try:
            num_dice = int(input())
            if not 1 <= num_dice <= 10:
                raise ValueError
            self.sound_manager.play('select')
        except ValueError:
            self.sound_manager.play('failure')
            print(Fore.RED + "[ERRO] Número inválido de módulos. Pressione Enter...")
            input()
            return
        
        rolls = self.roll_dice(num_dice)
        max_roll = max(rolls) if rolls else 0
        
        self.display_rolling_animation(rolls)
        
        if self.current_hack.code == "QUANTUM_CRACK":
            if max_roll >= 5:
                self.sound_manager.play('success')
                self.quantum_crack_success(max_roll)
            else:
                self.sound_manager.play('alert')
                self.display_failure()
        else:
            success_count = sum(1 for roll in rolls if roll >= 5)
            critical_success = any(roll == 6 for roll in rolls)
            
            if critical_success:
                self.sound_manager.play('success')
                self.display_success()
            elif success_count > 0:
                self.sound_manager.play('success')
                self.display_partial_success()
            else:
                self.sound_manager.play('alert')
                self.display_failure()

    def display_success(self):
        messages = [
            "╔══════════════════════════════╗",
            "║     ACESSO TOTAL OBTIDO      ║",
            "╚══════════════════════════════╝",
            "[FIREWALL NEUTRALIZADO]",
            "[DADOS BAIXADOS COM SUCESSO]",
            "[ADMINISTRADOR ROOT OBTIDO]",
            f"[IP MASCARADO]: {self.generate_random_ip()}",
            "[RASTROS DIGITAIS ELIMINADOS]"
        ]
        
        for msg in messages:
            self.print_fast(msg, Fore.GREEN)
            time.sleep(0.2)
        
        print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
        input()

    def display_partial_success(self):
        messages = [
            "╔══════════════════════════════╗",
            "║    ACESSO PARCIAL OBTIDO     ║",
            "╚══════════════════════════════╝",
            "[ALERTA: DETECÇÃO PARCIAL]",
            "[SISTEMAS DE SEGURANÇA ATIVOS]",
            f"[IP DETECTADO]: {self.generate_random_ip()}",
            "[FIREWALL PARCIALMENTE ATIVO]"
        ]
        
        for msg in messages:
            self.print_fast(msg, Fore.YELLOW)
            time.sleep(0.2)
        
        print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
        input()

    def display_failure(self):
        self.menu_manager.clear_screen()
        messages = [
            "╔══════════════════════════════╗",
            "║      !!! ALERTA !!!          ║",
            "╚══════════════════════════════╝",
            "[FALHA CRÍTICA DE ACESSO]",
            "[ICE BLACK DETECTADO]",
            "[CONTRAMEDIDAS ATIVADAS]",
            f"[IP COMPROMETIDO]: {self.generate_random_ip()}",
            "[ALERTANDO NETWATCH...]",
            "[TRAÇADORES CORPORATIVOS ATIVOS]"
        ]
        
        for msg in messages:
            self.print_fast(msg, Fore.RED)
            time.sleep(0.2)
        
        print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
        input()

    def quantum_crack_success(self, max_roll):
        if max_roll == 6:
            correct_code = self.generate_security_code()
            messages = [
                "╔═════════════════════════════════════╗",
                "║    DECODIFICAÇÃO QUÂNTICA: ÊXITO    ║",
                "╚═════════════════════════════════════╝",
                "[SENHA DECODIFICADA COM SUCESSO]",
                f"[CÓDIGO DE ACESSO]: {correct_code}",
                "[ACESSO GARANTIDO]"
            ]
            
            for msg in messages:
                self.print_fast(msg, Fore.GREEN)
                time.sleep(0.2)
            
            print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
            input()
                
        elif max_roll == 5:
            correct_code = self.generate_security_code()
            fake_codes = [self.generate_security_code() for _ in range(3)]
            all_codes = fake_codes + [correct_code]
            random.shuffle(all_codes)
            
            self.menu_manager.clear_screen()
            messages = [
                "╔═════════════════════════════════════╗",
                "║    DECODIFICAÇÃO PARCIAL: ALERTA    ║",
                "╚═════════════════════════════════════╝",
                "[SEQUÊNCIAS POTENCIAIS DETECTADAS]",
                "[VOCÊ TEM 3 TENTATIVAS]"
            ]
            
            for msg in messages:
                self.print_fast(msg, Fore.YELLOW)
                time.sleep(0.2)
            
            print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
            input()
            
            attempts = 3
            while attempts > 0:
                selected = self.select_code_menu(all_codes, attempts)
                selected_code = all_codes[selected]
                
                if selected_code == correct_code:
                    self.sound_manager.play('success')
                    messages = [
                        "╔═════════════════════════════════════╗",
                        "║         CÓDIGO CORRETO!!!           ║",
                        "╚═════════════════════════════════════╝",
                        "[DECODIFICAÇÃO BEM-SUCEDIDA]",
                        f"[CÓDIGO VALIDADO]: {selected_code}",
                        "[ACESSO GARANTIDO]"
                    ]
                    self.menu_manager.clear_screen()
                    for msg in messages:
                        self.print_fast(msg, Fore.GREEN)
                        time.sleep(0.2)
                    print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
                    input()
                    return
                else:
                    self.sound_manager.play('failure')
                    attempts -= 1
                    if attempts > 0:
                        error_messages = [
                            "╔═════════════════════════════════════╗",
                            "║         CÓDIGO INCORRETO!           ║",
                            "╚═════════════════════════════════════╝",
                            f"[TENTATIVAS RESTANTES]: {attempts}"
                        ]
                        self.menu_manager.clear_screen()
                        for msg in error_messages:
                            self.print_fast(msg, Fore.RED)
                        print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONTINUAR]")
                        input()
                    else:
                        self.sound_manager.play('alert')
                        self.display_failure()

    def select_code_menu(self, codes: List[str], attempts_left: int) -> int:
        selected = 0
        while True:
            self.menu_manager.clear_screen()
            print(Fore.CYAN + "╔═════════════════════════════════════╗")
            print(Fore.CYAN + "║    SELECIONE O CÓDIGO DE ACESSO     ║")
            print(Fore.CYAN + "╚═════════════════════════════════════╝\n")
            
            print(Fore.GREEN + f"[TENTATIVAS RESTANTES]: {attempts_left}\n")
            
            for i, code in enumerate(codes):
                if i == selected:
                    print(Fore.GREEN + "► " + code + " ◄")
                else:
                    print(Fore.CYAN + "  " + code + "  ")
            
            print("\n" + Fore.YELLOW + "[USE ↑↓ PARA NAVEGAR E ENTER PARA SELECIONAR]")
            
            key = self.menu_manager.wait_key()
            if key == 'up' and selected > 0:
                selected -= 1
                self.sound_manager.play('move')
            elif key == 'down' and selected < len(codes) - 1:
                selected += 1
                self.sound_manager.play('move')
            elif key == 'enter':
                self.sound_manager.play('select')
                return selected

    def run(self):
        self.startup_sequence()
        while self.running:
            choice = self.main_menu()
            if choice == 0:  # Iniciar Exploit
                self.simulate_hack_attempt()
            else:  # Desconectar da Matrix
                self.running = False
                self.menu_manager.clear_screen()
                self.print_fast("[DESCONECTANDO DA MATRIX...]", Fore.CYAN)
                self.sound_manager.play('shutdown')
                print("\n" + Fore.YELLOW + "[PRESSIONE ENTER PARA CONFIRMAR DESCONEXÃO]")
                input()
                self.menu_manager.clear_screen()
                self.print_fast("[CONEXÃO ENCERRADA - ATÉ A PRÓXIMA, RUNNER]", Fore.RED)
                time.sleep(2)
                break

def main():
    try:
        terminal = CyberTerminal()
        terminal.run()
    except ImportError:
        print("Instalando dependências necessárias...")
        os.system('pip install colorama keyboard pygame')
        terminal = CyberTerminal()
        terminal.run()

if __name__ == "__main__":
    main()