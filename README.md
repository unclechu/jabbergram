<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline13">1. jabbergram</a>
<ul>
<li><a href="#orgheadline6">1.1. English</a>
<ul>
<li><a href="#orgheadline1">1.1.1. About</a></li>
<li><a href="#orgheadline2">1.1.2. Installation</a></li>
<li><a href="#orgheadline3">1.1.3. Configuration</a></li>
<li><a href="#orgheadline4">1.1.4. Usage</a></li>
<li><a href="#orgheadline5">1.1.5. License</a></li>
</ul>
</li>
<li><a href="#orgheadline12">1.2. Castellano</a>
<ul>
<li><a href="#orgheadline7">1.2.1. Acerca de</a></li>
<li><a href="#orgheadline8">1.2.2. Instalación</a></li>
<li><a href="#orgheadline9">1.2.3. Configuración</a></li>
<li><a href="#orgheadline10">1.2.4. Uso</a></li>
<li><a href="#orgheadline11">1.2.5. Licencia</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>

# jabbergram<a id="orgheadline13"></a>

## English<a id="orgheadline6"></a>

### About<a id="orgheadline1"></a>

With this program, it's possible to use a MuC `XMPP` room to talk to a group on `Telegram` and vice versa. The aim of this program is to be just a simple gateway, just pass text from one way to the other. Once it's stable, it probably won't have more improvements, since I don't need them.

Since version 0.1.6, Jabbergram has HTTP Upload support. If the server supports it, it will automatically upload all the files sent to the Telegram group.

### Installation<a id="orgheadline2"></a>

As with any program that uses python, it should be used a virtual environment (virtualenv), but that is user selectable. It's possible to use one of the next installation methods:

Install via pip:

    $ su -c "pip3 install jabbergram"

Clone the repository:

    $ git clone git://daemons.cf/jabbergram
    $ cd jabbergram
    $ su -c "pip3 install -r requirements.txt"
    $ su -c "python3 setup.py install"

### Configuration<a id="orgheadline3"></a>

This program is simple, it even doesn't have a `help` menu. First thing you need to do is to create `Telegram` Bot. To do so, you must have a telegram account and talk to [BotFather](https://telegram.me/botfather). Then, execute:

    /start
    /newbot
    YourNameBot # ended in bot, always
    # then it will show your bot token, save it
    /setprivacy
    YourNameBot
    # now press Disable

The `/setprivacy` option is to make the bot read all what it's said to him, not only when using commands. It's necessary to make `jabbergram` work. More info on creating `Telegram` bots at their [webpage](https://core.telegram.org/bots).

Then, you will have to create a config file. We'll call it `config.ini`. In that file, enter the next parameters:

    [config]
    jid = exampleJid@nope.org
    password = difficultPassword
    muc_room = exampleMuc@muc.nope.org
    nick = jabbergram
    token = jabbergramBotTokken
    group = -10293943920

The only thing worth mentioning is the `token` section, which is said to you when creating the bot, and the `group`, that is the `Telegram` group ID.

There's no easy way to see this from telegram, so you can use the separate utility called `seeIdGroups.py`. To execute it, you only need to set the `token` parameter in the config file. You will need that somebody invite the bot to the group. Also, people on that group must send some messages, so the utility can grab it's id. It may take a couple. When you have the group ID you want, just press Ctrl-c, copy it to the config file (even the minus symbol), and the configuration will be done.

### Usage<a id="orgheadline4"></a>

There only can be one configuration file. This is because it can only be one bot connection, when there's more than one, message are lost. Therefore, for linking more rooms you must "link" them in the configuration. This is done simply by hooking jabber rooms with Telegram:

    [Config]
    JID = exampleJid@nope.org
    password = difficultPassword
    muc_room = exampleMuc@muc.nope.org segunda@muc.sip.org
    nick = jabbergram
    token = jabbergramBotTokken
    group = -10293943920 120301203

Thus, the example's muc "exampleMuc@muc.nope.org" syncs with the group "-10293943920" and "segunda@muc.sip.org" with "120 301203".

### License<a id="orgheadline5"></a>

    This program is free software: you can redistribute it and / or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, Either version 3 of the License, or
    (At your option) any later version.

    This program is distributed in the hope That it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    Along With This Program. If not, see <http://www.gnu.org/licenses/>.

## Castellano<a id="orgheadline12"></a>

### Acerca de<a id="orgheadline7"></a>

Con este programa es posible utilizar una sala `XMPP` para hablar con un grupo de `Telegram` y viceversa. El objetivo de este programa es el de ser sólo una pasarela sencilla, sólo tiene que pasar el texto de un lado al otro. Una vez que sea estable, probablemente no tendrá más mejoras, ya que yo no las necesito.

Desde la versión 0.1.6, Jabbergram tiene soporte HTTP Upload. Si el servidor lo soporta, subirá automáticamente todos los archivos enviados desde el grupo de Telegram.

### Instalación<a id="orgheadline8"></a>

Como con cualquier programa escrito en `Python`, deberia ser usado en un entorno virtual (virtualenv), pero eso queda a la elección del usuario. Es posible utilizar uno de los siguientes métodos de instalación:

Instalar a través de `pip`:

    $ su -c "pip3 instalar jabbergram"

Clonar el repositorio:

    $ git clone git://daemons.cf/jabbergram
    $ cd jabbergram
    $ su -c "pip3 instalar -r requirements.txt"
    $ su -c "python3 setup.py install"

### Configuración<a id="orgheadline9"></a>

Este programa es simple, no tiene ni un menú de `ayuda`. Lo primero que hay que hacer es crear el bot de `Telegram`. Para ello, hay que tener una cuenta de `Telegram` y hablar con [BotFather](https://telegram.me/botfather). A continuación, ejecuta:

    /start
    /newbot
    NombreDelBot # terminado en bot, siempre
    # A continuación, se mostrará el token del bot, hay que guardarlo
    /setprivacy
    NombreDelBot
    # Ahora hay que pulsar desactivar

La opción `/setprivacy` es para hacer que el robot pueda leer todo lo que se dice en el grupo, no sólo cuando se utilizan los comandos. Es necesario para hacer que `jabbergram` funcione. Más información sobre la creación los bots de `Telegrama` en su [página web](https://core.telegram.org/bots).

A continuación, hay que crear un archivo de configuración, que llamaremos `config.ini`. En ese archivo, introduce los siguientes parámetros:

    [Config]
    JID = exampleJid@nope.org
    password = difficultPassword
    muc_room = exampleMuc@muc.nope.org
    nick = jabbergram
    token = jabbergramBotTokken
    group = -10,293,943,920

La única cosa que vale la pena mencionar es la sección del `token` (que es la que nos da cuando se crea el robot) y el `group`, que es ID del grupo de `Telegram`.

No hay manera fácil de ver el ID desde `Telegram`, por lo que se puede utilizar el programa llamado `seeIdGroups.py`. Para ejecutarlo sólo es necesario establecer el parámetro `token` del archivo de configuración. Necesitarás que alguien invite al bot al grupo. Además, las personas de ese grupo deben enviar algunos mensajes, para que el programa pueda coger su ID. Puede llevar unos segundos el que aparezcan los mensajes. Cuando se tenga el ID de grupo que se quiere, sólo hay que pulsar Ctrl-c, copiarlo en el archivo de configuración (incluido el simbolo menos), y la configuración estará terminada.

### Uso<a id="orgheadline10"></a>

Sólo puede haber un archivo de configuración. Esto es debido a que sólo puede haber una conexión del bot, cuando hay más de una se pierden mensajes. Por lo tanto, para linkear más salas hay que "linkearlas" en la configuración. Esto se hace, simplemente, enganchando las salas de jabber con las de telegram:

    [Config]
    JID = exampleJid@nope.org
    password = difficultPassword
    muc_room = exampleMuc@muc.nope.org segunda@muc.sip.org
    nick = jabbergram
    token = jabbergramBotTokken
    group = -10293943920 120301203

De este modo, el muc "exampleMuc@muc.nope.org" se sincronizará con el grupo "-10293943920", y "segunda@muc.sip.org" con "120301203".

### Licencia<a id="orgheadline11"></a>

    This program is free software: you can redistribute it and / or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, Either version 3 of the License, or
    (At your option) any later version.

    This program is distributed in the hope That it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    Along With This Program. If not, see <http://www.gnu.org/licenses/>.
