![Logo](img/logo.jpeg)

# Projeto Identifica

Projeto realizado pelo IFRS-Erechim, UFFS-Erechim e URI-Erchim em parceria com a Prefeitura da Cidade, visando elaborar um diagnóstico socioeconômico de Erechim.

Objetivo: Propor um modelo de atuação integrado para o município de Erechim, articulando diretrizes regionais, capacidades locais e mecanismos de monitoramento por indicadores, com foco na competitividade e no desenvolvimento sustentável.

# Identifica Dashboard

Dashboard integrando dados públicos de Erechim de diversas fontes.

## Como rodar

Você vai precisar de `git` e `docker`.

1. Clone o repositório e acesse a pasta dele na sua máquina

```sh
git clone https://github.com/IDENTIFICA-ERECHIM/identifica-dashboard.git
```

2. Certifique-se de que o banco esta rodando. Isso acontece no identifica-etl

```sh
cd identifica-etl
docker compose up -d mysql
```

3. Configure o `.env` com base no `.env.example`

4. Rodar

- No linux, rode o script `rodar.sh`

```sh
chmod +x
./rodar.sh
```

- No windows, rode o script `rodar.bat`

```powershell
.\rodar.bat
```

---

Com o dashboard rodando, qualquer pessoa conectada na mesma rede pode acessar.

O dashboard fica disponível na porta `8501` do computador que está rodando o Docker, e é possível acessar pelo IP deste computador.


Para descobrir o ip do seu computador, use:

- Linux:

```sh
hostname -I
```

O primeiro número costuma ser o IP da sua rede local

- Windows:

```powershell
ipconfig
```

Procure o adaptador que você está usando (Wi-Fi ou Ethernet) e anote o Endereço IPv4


- Para acessar, então, use:

```
http://DIGITE_O_IP_AQUI:8501
```


Caso o firewall do windows estiver bloqueando o acesso, digite, no powershell como admin, para liberar a porta:

```powershell
New-NetFirewallRule -DisplayName "Identifica Dashboard" -Direction Inbound -Protocol TCP -LocalPort 8501 -Action Allow -Profile Private
```

Se quiser desfazer depois, rode:

```powershell
Remove-NetFirewallRule -DisplayName "Identifica Dashboard"
```
