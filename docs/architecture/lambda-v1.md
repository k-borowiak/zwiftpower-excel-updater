# Lambda architecture v1

## Cel
Wstępny szkic architektury AWS dla projektu ZwiftPower Excel Updater.

## Główne elementy
- ECR – przechowuje obraz kontenera dla funkcji Lambda
- Lambda – wykonuje logikę aplikacji
- EventBridge Scheduler – uruchamia zadanie okresowo
- Parameter Store – przechowuje ZP_USERNAME i ZP_PASSWORD
- S3 – przechowuje plik wejściowy i wynikowy
- CloudWatch Logs – przechowuje logi wykonania

## Założenia runtime
- timeout Lambdy: 840 s
- soft stop w kodzie: 800 s
- pamięć tymczasowa (/tmp): 2048 MB

## Input / Output
- input: `team.xlsx` w S3
- output: `updated_team.xlsx` w S3

## Uwagi
To jest pierwsza robocza wersja architektury pod dalsze prace nad Terraformem.