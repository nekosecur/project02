import re
from pyrogram import Client, types, enums
from plugins import Database
import config  # Pastikan untuk mengimpor konfigurasi Anda

async def member_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)

    if re.search(r"^[\/]addmember(\s|\n)*$", msg.text or msg.caption):
        # Hanya izinkan admin
        if msg.from_user.id != config.id_admin:
            return

        return await msg.reply_text(
            text="<b>Cara penggunaan tambah member</b>\n\n<code>/addmember id_user</code>\n\nContoh :\n<code>/addmember 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    if re.search(r"^[\/]hapusmember(\s|\n)*$", msg.text or msg.caption):
        # Hanya izinkan admin
        if msg.from_user.id != config.id_admin:
            return

        return await msg.reply_text(
            text="<b>Cara penggunaan hapus member</b>\n\n<code>/hapusmember id_user</code>\n\nContoh :\n<code>/hapusmember 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

async def tambah_member_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)

    if not (y := re.search(r"^[\/]addmember(\s|\n)*(\d+)$", msg.text or msg.caption)):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah member</b>\n\n<code>/addmember id_user</code>\n\nContoh :\n<code>/addmember 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    target = int(y[2])
    db = Database(target)

    # Hanya izinkan admin
    if msg.from_user.id != config.id_admin:
        return

    # Periksa apakah pengguna diblokir atau tidak terdaftar di database
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadi member",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> tidak terdaftar di database</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    # Periksa status pengguna
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()

    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi member</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    try:
        a = await client.get_users(target)
        nama = await helper.escapeHTML(
            f'{a.first_name} {a.last_name}' if a.last_name else a.first_name
        )

        await db.addmember(target)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi member</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
