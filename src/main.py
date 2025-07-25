from public_object import log, config, adb_path, ocr_pic
from adb_service import check_adb_path, check_adb_device
from circle_logic import match_only, do_circle, safe_exit, delete_old_screenshots
from lin_simulator import LiveState
from src.smart_policy import SmartPolicy


flower_money = 1
balance_money = 5
fierce_money = 4

throw_count = 3
ticket_cost = 2

silk_cocoon = False
stay_prob = 0.6


if __name__ == "__main__":

    log("-" * 100)
    log(f"读取到配置：{config}")

    # 检查adb路径
    if not check_adb_path(adb_path):
        log("adb.exe路径错误，请检查并替换正确的路径")
        safe_exit(1)

    # 检查adb服务
    if not check_adb_device(adb_path):
        log("未检测到已连接的模拟器或设备，请先启动MuMu模拟器并确保adb可用。")
        safe_exit(1)

    if not match_only(ocr_pic['小常乐']):
        log("未识别到常乐节点")
        safe_exit(1)

    live_state = LiveState(
        candle=0, originium=0, tickets=0,
        flower_money=flower_money, balance_money=balance_money, fierce_money=fierce_money,
        throw_count=throw_count, ticket_cost=ticket_cost, silk_cocoon=silk_cocoon, prize_count=0,
        stay_prob=stay_prob, money_box=['花'] * flower_money + ['衡'] * balance_money + ['厉'] * fierce_money
    )

    policy = SmartPolicy()  # 启动智能决策系统

    # 主循环
    while True:
        res = do_circle(live_state, policy)
        if res == 1:
            break

        delete_old_screenshots()
        log("清除超时的旧截图文件")

    safe_exit(0)
