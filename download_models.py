import os
import sys
import requests
from tqdm import tqdm  # для красивого прогресс-бара (опционально)

def download_file(url, local_path):
    """Скачивает файл с прогресс-баром"""
    try:
        # Проверяем, есть ли уже частично скачанный файл
        resume_header = {}
        if os.path.exists(local_path):
            resume_header = {'Range': f'bytes={os.path.getsize(local_path)}-'}

        response = requests.get(url, stream=True, headers=resume_header, timeout=30)
        response.raise_for_status()

        # Получаем общий размер файла
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192

        # Режим дозаписи, если файл уже частично скачан
        mode = 'ab' if resume_header else 'wb'

        with open(local_path, mode) as f:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                      desc=os.path.basename(local_path)) as pbar:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        return True
    except Exception as e:
        print(f"❌ Ошибка загрузки {os.path.basename(local_path)}: {e}")
        return False

def download_models():
    """Скачивает все необходимые модели"""
    models = [
        "gen_1_q_table_and_params_4901.pkl",
        "gen_2_q_table_and_params_4901.pkl"
    ]

    base_url = "https://huggingface.co/Annuta/ping_pong_with_AI/resolve/main/"
    local_dir = "tables"

    # Создаём папку для моделей
    os.makedirs(local_dir, exist_ok=True)

    print("📥 Проверка файлов моделей...")
    all_success = True

    for model in models:
        local_path = os.path.join(local_dir, model)
        url = base_url + model

        if not os.path.exists(local_path):
            print(f"\n   Загрузка {model}...")
            if download_file(url, local_path):
                print(f"   ✅ {model} загружен")
            else:
                all_success = False
        else:
            # Проверяем размер (на всякий случай)
            file_size = os.path.getsize(local_path) / (1024*1024)
            print(f"   ✅ {model} уже есть ({file_size:.1f} МБ)")

    return all_success

if __name__ == "__main__":
    # Пытаемся импортировать tqdm для прогресс-бара, но не падаем если нет
    try:
        from tqdm import tqdm
    except ImportError:
        # Создаём заглушку для tqdm
        class tqdm:
            def __init__(self, *args, **kwargs):
                pass
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def update(self, n):
                pass

    success = download_models()
    sys.exit(0 if success else 1)
