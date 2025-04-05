from pkg.platform.types import MessageChain
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
from plugins.HelloPlugin.utils.message_adapter import FileUploader
from pathlib import Path
import re


# 注册插件
@register(name="test_file_sender", description="测试发送文件", version="1.0", author="drdon1234")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        super().__init__(host)
        config_path = Path(__file__).parent / "config.yaml"
        self.uploader = FileUploader(config_path)

    # 异步初始化
    async def initialize(self):
        pass

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def message_received(self, ctx: EventContext):
        receive_text = ctx.event.text_message
        cleaned_text = re.sub(r'@\S+\s*', '', receive_text).strip()
        prevent_default = True
        if cleaned_text.startswith('测试发送文件'):
            await self.do_test_upload_file(ctx)
        else:
            prevent_default = False
        if prevent_default:
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass

    # 测试发送文件
    async def do_test_upload_file(self, ctx: EventContext):
        await self.uploader.upload_file(ctx, "/app/sharedFolder", "test.pdf")
