# test_methods.py
from core.screen_capturer import ScreenCapturer

capturer = ScreenCapturer()
print("🔍 Métodos disponibles en ScreenCapturer:")
print("=" * 40)

methods = [m for m in dir(capturer) if not m.startswith('_')]
for method in sorted(methods):
    print(f"  • {method}")

print(f"\n📊 Total: {len(methods)} métodos")