from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

_REGISTERED_CHINESE_FONT = None  # 缓存已注册的中文字体名称，避免重复注册

def ensure_font(font_name: str = "SimHei", font_path: str | None = None) -> str:
    """确保注册一个支持中文的字体并返回其名称。

    优先顺序：
    1. 如果已经注册过，直接返回。
    2. 使用用户提供的 font_path。
    3. 自动搜索常见 Windows 中文字体路径。
    4. 回退到 Helvetica-Bold（会导致中文显示为空）。

    使用提示：将所需字体文件 (例如 simhei.ttf 或 msyh.ttc) 放到脚本同目录，或修改传入的 font_path。
    """
    global _REGISTERED_CHINESE_FONT
    if _REGISTERED_CHINESE_FONT:
        return _REGISTERED_CHINESE_FONT

    # 已注册则无需重复
    if font_name in pdfmetrics.getRegisteredFontNames():
        _REGISTERED_CHINESE_FONT = font_name
        return font_name

    candidate_paths = []
    if font_path:
        candidate_paths.append(font_path)
    # 常见字体候选（按常用优先）
    candidate_paths.extend([
        os.path.join(os.getcwd(), "simhei.ttf"),
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\SourceHanSansSC-Regular.otf",
    ])

    chosen = None
    for p in candidate_paths:
        if p and os.path.exists(p):
            chosen = p
            break

    if chosen:
        try:
            pdfmetrics.registerFont(TTFont(font_name, chosen))
            _REGISTERED_CHINESE_FONT = font_name
            print(f"🈶 已注册中文字体: {font_name} -> {chosen}")
            return font_name
        except Exception as e:
            print(f"⚠️ 注册字体失败 {chosen}: {e}. 回退到英文字体 Helvetica-Bold，中文将无法显示。")
    else:
        print("⚠️ 未找到中文字体文件，回退到英文字体 Helvetica-Bold，中文水印可能为空。请放置 simhei.ttf 到脚本目录或指定 font_path。")

    _REGISTERED_CHINESE_FONT = "Helvetica-Bold"
    return _REGISTERED_CHINESE_FONT

def create_watermark(
    text: str,
    *,
    angle: float = 45,
    font_name: str | None = None,
    font_size: int = 40,
    fill_gray: float = 0.5,
    alpha: float = 0.18,
    gap_x: int = 300,
    gap_y: int = 240,
    offset_x: int = 0,
    offset_y: int = 0,
) -> PdfReader:
    """生成包含多处重复文字水印的单页 PDF。

    参数：
    - text: 水印文字（支持中文）
    - angle: 文字旋转角度（度）
    - font_name: 指定已注册字体名；None 时自动注册中文字体
    - font_size: 字号
    - fill_gray: 文字灰度（0黑-1白）
    - alpha: 透明度（0-1）
    - gap_x/gap_y: 网格间距（单位：pt，A4约为 595x842pt）
    - offset_x/offset_y: 网格整体偏移（用于微调与避免重叠）
    """

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # 字体
    if not font_name:
        font_name = ensure_font()
    can.setFont(font_name, font_size)

    # 颜色与透明度
    can.setFillGray(fill_gray, alpha)

    width, height = A4

    # 为了在旋转后仍覆盖全页，取稍大范围的网格
    start_x = -width + offset_x
    end_x = width * 2
    start_y = -height + offset_y
    end_y = height * 2

    # 绘制网格重复水印
    y = start_y
    while y <= end_y:
        x = start_x
        while x <= end_x:
            can.saveState()
            can.translate(x, y)
            can.rotate(angle)
            can.drawCentredString(0, 0, text)
            can.restoreState()
            x += gap_x
        y += gap_y

    can.save()
    packet.seek(0)
    return PdfReader(packet)

def add_text_watermark(
    input_pdf: str,
    output_pdf: str,
    watermark_text: str,
    **watermark_opts,
):
    """给输入 PDF 每一页添加重复文字水印。

    watermark_opts 透传给 create_watermark，例如：
    angle=45, font_size=36, gap_x=320, gap_y=260, alpha=0.15, offset_x=0, offset_y=0
    """
    pdf = PdfReader(input_pdf)
    writer = PdfWriter()

    watermark = create_watermark(watermark_text, **watermark_opts)
    watermark_page = watermark.pages[0]

    for page in pdf.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"✅ 成功为 {input_pdf} 添加水印，输出文件：{output_pdf}")

if __name__ == "__main__":
    # ======== 用户自定义部分 ========
    input_pdf = "input.pdf"                  # 原 PDF 路径
    output_pdf = "output_with_watermark.pdf"  # 输出 PDF 路径
    watermark_text = "仅供材料核对"           # 水印文字（支持中文）
    # 可选：自定义字体路径（若自动未找到）
    # ensure_font(font_path=r"C:\Windows\Fonts\simhei.ttf")

    # 重复水印参数示例：
    opts = dict(
        angle=45,        # 旋转角度
        font_size=38,    # 字号
        fill_gray=0.5,   # 颜色灰度
        alpha=0.16,      # 透明度
        gap_x=300,       # 横向间隔（pt）
        gap_y=240,       # 纵向间隔（pt）
        offset_x=0,      # 横向偏移（pt）
        offset_y=0,      # 纵向偏移（pt）
    )
    # =================================

    add_text_watermark(input_pdf, output_pdf, watermark_text, **opts)
