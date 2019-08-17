from kodipydent import Kodi


def radio_play():
    my_kodi = Kodi('127.0.0.1', username='kodi', password='asillydoodleding', port=8080)
    addon = my_kodi.Addons.ExecuteAddon('plugin.audio.radio_de')
    open_radio = my_kodi.Player.Open(item={"file": "plugin://plugin.audio.radio_de/station/2220"})


def kodi_stop():
    my_kodi = Kodi('127.0.0.1', username='kodi', password='asillydoodleding', port=8080)
    try:
        _playerid = my_kodi.Player.GetActivePlayers()['result'][0]['playerid']
    except IndexError:
        return
    my_kodi.Player.Stop(_playerid)


def kodi_start():
    my_kodi = Kodi('127.0.0.1', username='kodi', password='asillydoodleding', port=8080)
    try:
        _playerid = my_kodi.Player.GetActivePlayers()['result'][0]['playerid']
    except IndexError:
        return
    my_kodi.Player.Start(_playerid)


