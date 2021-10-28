from bilibili_api import user, sync
import json

u = user.User(703007996)
async def main():
    offset = 0
    page = await u.get_dynamics(offset)
    with open ('./test.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(page,indent=2,ensure_ascii=False))

sync(main())