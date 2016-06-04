-  `ended in bot, always <#ended-in-bot,-always>`__
-  `+BEGIN\_SRC text <#+begin_src-text>`__
-  `+END\_SRC <#+end_src>`__

ended in bot, always
====================

::

      # then it will show your bot token, save it
      /setprivacy
      YourNameBot
      # now press Disable
    #+END_SRC

    The =/setprivacy= option is to make the bot read all what it's said to him, not only when using commands. It's necessary to make =jabbergram= work. More info on creating =Telegram= bots at their [[https://core.telegram.org/bots][webpage]].

    Then, you will have to create a config file. We'll call it =config.ini=. In that file, enter the next parameters:

    #+BEGIN_SRC text
      [config]
      jid = exampleJid@nope.org
      password = difficultPassword
      muc_room = exampleMuc@muc.nope.org
      nick = jabbergram
      token = jabbergramBotTokken
      group = -10293943920
    #+END_SRC

    The only thing worth mentioning is the =token= section, which is said to you when creating the bot, and the =group=, that is the =Telegram= group ID.

    There's no easy way to see this from telegram, so you can use the separate utility called =seeIdGroups.py=. To execute it, you only need to set the =token= parameter in the config file. You will need that somebody invite the bot to the group. Also, people on that group must send some messages, so the utility can grab it's id. It may take a couple. When you have the group ID you want, just press Ctrl-c, copy it to the config file (even the minus symbol), and the configuration will be done.

\*\*\* Usage There only can be one configuration file. This is because
it can only be one bot connection, when there's more than one, message
are lost. Therefore, for linking more rooms you must "link" them in the
configuration. This is done simply by hooking jabber rooms with
Telegram:

::

    #+BEGIN_SRC sh
      [Config]
      JID = exampleJid@nope.org
      password = difficultPassword
      muc_room = exampleMuc@muc.nope.org segunda@muc.sip.org
      nick = jabbergram
      token = jabbergramBotTokken
      group = -10293943920 120301203
    #+END_SRC

    Thus, the example's muc "exampleMuc@muc.nope.org" syncs with the group "-10293943920" and "segunda@muc.sip.org" with "120 301203".

\*\*\* License #+BEGIN\_SRC text This program is free software: you can
redistribute it and / or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, Either
version 3 of the License, or (At your option) any later version.

::

      This program is distributed in the hope That it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
      GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
      Along With This Program. If not, see <http://www.gnu.org/licenses/>.
    #+END_SRC

\*\* Castellano \*\*\* Acerca de Con este programa es posible utilizar
una sala =XMPP= para hablar con un grupo de =Telegram= y viceversa. El
objetivo de este programa es el de ser sólo una pasarela sencilla, sólo
tiene que pasar el texto de un lado al otro. Una vez que sea estable,
probablemente no tendrá más mejoras, ya que yo no las necesito. \*\*\*
Instalación Como con cualquier programa escrito en =Python=, deberia ser
usado en un entorno virtual (virtualenv), pero eso queda a la elección
del usuario. Es posible utilizar uno de los siguientes métodos de
instalación:

::

     Instalar a través de =pip=:
     #+BEGIN_SRC sh
       $ su -c "pip3 instalar jabbergram"
     #+END_SRC

     Clonar el repositorio:
     #+BEGIN_SRC sh
       $ git clone git://daemons.cf/jabbergram
       $ cd jabbergram
       $ su -c "pip3 instalar requirements.txt -r"
       $ su -c "python3 setup.py instalar"
     #+END_SRC

\*\*\* Configuración Este programa es simple, no tiene ni un menú de
=ayuda=. Lo primero que hay que hacer es crear el bot de =Telegram=.
Para ello, hay que tener una cuenta de =Telegram= y hablar con
[[https://telegram.me/botfather][BotFather]]. A continuación, ejecuta:

::

    #+BEGIN_SRC sh
      /start
      /newbot
      NombreDelBot # terminado en bot, siempre
      # A continuación, se mostrará el token del bot, hay que guardarlo
      /setprivacy
      NombreDelBot
      # Ahora hay que pulsar desactivar
    #+END_SRC

    La opción =/setprivacy= es para hacer que el robot pueda leer todo lo que se dice en el grupo, no sólo cuando se utilizan los comandos. Es necesario para hacer que =jabbergram= funcione. Más información sobre la creación los bots de =Telegrama= en su [[https://core.telegram.org/bots][página web]].

    A continuación, hay que crear un archivo de configuración, que llamaremos =config.ini=. En ese archivo, introduce los siguientes parámetros:

    #+BEGIN_SRC text
      [Config]
      JID = exampleJid@nope.org
      password = difficultPassword
      muc_room = exampleMuc@muc.nope.org
      nick = jabbergram
      token = jabbergramBotTokken
      group = -10,293,943,920
    #+END_SRC

    La única cosa que vale la pena mencionar es la sección del =token= (que es la que nos da cuando se crea el robot) y el =group=, que es ID del grupo de =Telegram=.

    No hay manera fácil de ver el ID desde =Telegram=, por lo que se puede utilizar el programa llamado =seeIdGroups.py=. Para ejecutarlo sólo es necesario establecer el parámetro =token= del archivo de configuración. Necesitarás que alguien invite al bot al grupo. Además, las personas de ese grupo deben enviar algunos mensajes, para que el programa pueda coger su ID. Puede llevar unos segundos el que aparezcan los mensajes. Cuando se tenga el ID de grupo que se quiere, sólo hay que pulsar Ctrl-c, copiarlo en el archivo de configuración (incluido el simbolo menos), y la configuración estará terminada.

\*\*\* Uso Sólo puede haber un archivo de configuración. Esto es debido
a que sólo puede haber una conexión del bot, cuando hay más de una se
pierden mensajes. Por lo tanto, para linkear más salas hay que
"linkearlas" en la configuración. Esto se hace, simplemente, enganchando
las salas de jabber con las de telegram:

+BEGIN\_SRC text
================

::

      [Config]
      JID = exampleJid@nope.org
      password = difficultPassword
      muc_room = exampleMuc@muc.nope.org segunda@muc.sip.org
      nick = jabbergram
      token = jabbergramBotTokken
      group = -10293943920 120301203

+END\_SRC
=========

De este modo, el muc "exampleMuc@muc.nope.org" se sincronizará con el
grupo "-10293943920", y "segunda@muc.sip.org" con "120301203". \*\*\*
Licencia #+BEGIN\_SRC text This program is free software: you can
redistribute it and / or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, Either
version 3 of the License, or (At your option) any later version.

::

      This program is distributed in the hope That it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
      GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
      Along With This Program. If not, see <http://www.gnu.org/licenses/>.
    #+END_SRC
