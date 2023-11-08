import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def tambah_anggota_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    if re.search(r"^[\/]addmember(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah anggota</b>\n\n<code>/addmember id_user</code>\n\nContoh :\n<code>/addmember 121212021</code>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    if not (
        y := re.search(
            r"^[\/]addmember(\s|\n)*(\d+)$", msg.text or msg.caption
        )
    ):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah anggota</b>\n\n<code>/addmember id_user</code>\n\nContoh :\n<code>/addmember 121212021</code>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> tidak terdaftar di database</i>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )

    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} dan tidak dapat ditambahkan sebagai anggota</i>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )

    try:
        a = await client.get_chat(target)
        nama = await helper.escapeHTML(
            f'{a.first_name} {a.last_name}' if a.last_name else a.first_name
        )
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah ditambahkan sebagai anggota bot</i>\n└Ditambahkan oleh : <a href='tg://openmessage?user_id={str(client.id_bot)}'>Bot</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_anggota(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil ditambahkan sebagai anggota bot</i>\n└Ditambahkan oleh : <a href='tg://openmessage?user_id={str(client.id_bot)}'>Bot</a>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True, parse_mode=enums.ParseMode.HTML
       )

async def hapus_anggota_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]hapusmember(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan hapus anggota</b>\n\n<code>/hapusmember id_user</code>\n\nContoh :\n<code>/hapusmember 121212021</code>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    if not (
        x := re.search(
            r"^[\/]hapusmember(\s|\n)*(\d+)$", msg.text or msg.caption
        )
    ):
        return await msg.reply_text(
            text="<b>Cara penggunaan hapus anggota</b>\n\n<code>/hapusmember id_user</code>\n\nContoh :\n<code>/hapusmember 121212021</code>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    target = x[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> tidak terdaftar di database</i>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    member = db.get_data_pelanggan()
    if member.status in ['owner', 'admin']:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} dan tidak dapat dihapus sebagai anggota</i>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )

    try:
        await client.send_message(
            int(target),
            text=f"<i>Maaf, kamu telah dihapus dari anggota bot</i>\n└Dihapus oleh : <a href='tg://openmessage?user_id={str(client.id_bot)}'>Bot</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.hapus_anggota(int(target), client.id_bot)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil dihapus sebagai anggota bot</i>\n└Dihapus oleh : <a href='tg://openmessage?user_id={str(client.id_bot)}'>Bot</a>",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True, parse_mode=enums.ParseMode.HTML
        )
