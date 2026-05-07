@echo off
echo Iniciando build do CrossyPython...
python -m PyInstaller --onefile --windowed ^
--add-data "assets;assets" ^
--add-data "musica_fundo.mp3;." ^
--add-data "som_colisao.wav;." ^
--add-data "som_ponto.OGG;." ^
--add-data "som_game_over.wav;." ^
--add-data "som_vitoria.wav;." ^
--add-data "som_item.wav;." ^
--name "CrossyPython" main.py
echo Build concluido!
pause