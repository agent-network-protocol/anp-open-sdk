#!/usr/bin/env python3
"""
统一配置系统测试脚本

测试内容：
1. 基本配置加载和访问
2. 属性访问和代码提示
3. 环境变量映射和类型转换
4. 路径解析和占位符替换
5. 敏感信息保护
6. 向后兼容性
"""

import os
import sys
import tempfile
from pathlib import Path

import logging
logger = logging.getLogger(__name__)
# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_basic_config_loading():
    """测试基本配置加载"""
    logger.info("\n=== 测试1: 基本配置加载 ===")

    try:
        from anp_open_sdk.config import config

        # 测试配置加载
        logger.info(f"✅ 配置文件路径: {config._config_file}")
        logger.info(f"✅ 项目根目录: {config.get_app_root()}")

        # 测试基本配置访问
        logger.info(f"✅ ANP SDK端口: {config.anp_sdk.port}")
        logger.info(f"✅ ANP SDK主机: {config.anp_sdk.host}")
        logger.info(f"✅ 调试模式: {config.anp_sdk.debug_mode}")

        return True
    except Exception as e:
        logger.error(f"❌ 基本配置加载失败: {e}")
        return False

def test_attribute_access():
    """测试属性访问"""
    logger.info("\n=== 测试2: 属性访问 ===")

    try:
        from anp_open_sdk.config import config

        # 测试多级属性访问
        logger.info(f"✅ LLM模型: {config.llm.default_model}")
        logger.info(f"✅ LLM最大Token: {config.llm.max_tokens}")
        logger.info(f"✅ 邮件SMTP端口: {config.mail.smtp_port}")

        # 测试智能体配置
        logger.info(f"✅ 演示智能体1: {config.anp_sdk.agent.demo_agent1}")
        logger.info(f"✅ 演示智能体2: {config.anp_sdk.agent.demo_agent2}")

        # 测试配置修改
        original_port = config.anp_sdk.port
        config.anp_sdk.port = 8080
        logger.info(f"✅ 修改端口: {original_port} -> {config.anp_sdk.port}")
        config.anp_sdk.port = original_port  # 恢复

        return True
    except Exception as e:
        logger.error(f"❌ 属性访问测试失败: {e}")
        return False

def test_environment_variables():
    """测试环境变量"""
    logger.info("\n=== 测试3: 环境变量映射 ===")

    try:
        from anp_open_sdk.config import config

        # 设置测试环境变量
        os.environ['ANP_DEBUG'] = 'true'
        os.environ['ANP_PORT'] = '8888'
        os.environ['TEST_VAR'] = 'hello world'

        # 重新加载环境变量
        config.env.reload()

        # 测试预定义环境变量
        logger.info(f"✅ 调试模式 (ANP_DEBUG): {config.env.debug_mode}")
        logger.info(f"✅ 端口 (ANP_PORT): {config.env.port}")
        logger.info(f"✅ 端口类型: {type(config.env.port)}")

        # 测试动态环境变量
        logger.info(f"✅ 测试变量 (TEST_VAR): {config.env.test_var}")

        # 测试系统环境变量
        if config.env.system_path:
            logger.info(f"✅ PATH路径数量: {len(config.env.system_path)}")
            logger.info(f"✅ 第一个PATH: {config.env.system_path[0]}")

        if config.env.home_dir:
            logger.info(f"✅ 用户主目录: {config.env.home_dir}")
            logger.info(f"✅ 主目录类型: {type(config.env.home_dir)}")

        return True
    except Exception as e:
        logger.error(f"❌ 环境变量测试失败: {e}")
        return False

def test_path_resolution():
    """测试路径解析"""
    logger.info("\n=== 测试4: 路径解析 ===")

    try:
        from anp_open_sdk.config import config

        # 测试占位符解析
        user_path = config.anp_sdk.user_did_path
        resolved_path = config.resolve_path(user_path)
        logger.info(f"✅ 原始路径: {user_path}")
        logger.info(f"✅ 解析后路径: {resolved_path}")
        logger.info(f"✅ 是否为绝对路径: {resolved_path.is_absolute()}")

        # 测试相对路径解析
        relative_path = config.resolve_path("test/data.json")
        logger.info(f"✅ 相对路径解析: {relative_path}")

        # 测试手动占位符
        manual_path = config.resolve_path("{APP_ROOT}/logs/test.log")
        logger.info(f"✅ 手动占位符: {manual_path}")

        return True
    except Exception as e:
        logger.error(f"❌ 路径解析测试失败: {e}")
        return False

def test_secrets():
    """测试敏感信息"""
    logger.info("\n=== 测试5: 敏感信息保护 ===")

    try:
        from anp_open_sdk.config import config

        # 设置敏感信息环境变量
        os.environ['OPENAI_API_KEY'] = 'sk-test-key-12345'
        os.environ['MAIL_PASSWORD'] = 'secret-password'

        # 测试敏感信息访问
        api_key = config.secrets.openai_api_key
        mail_pwd = config.secrets.mail_password

        logger.info(f"✅ API密钥存在: {api_key is not None}")
        logger.info(f"✅ 邮件密码存在: {mail_pwd is not None}")
        logger.info(f"✅ API密钥前缀: {api_key[:10] if api_key else 'None'}...")

        # 测试敏感信息不在普通配置中
        secrets_dict = config.secrets.to_dict()
        masked_secrets_dict = {key: '***' for key in secrets_dict}
        logger.info(f"✅ 敏感信息字典: {masked_secrets_dict}")

        return True
    except Exception as e:
        logger.error(f"❌ 敏感信息测试失败: {e}")
        return False

def test_path_tools():
    """测试路径工具"""
    logger.info("\n=== 测试6: 路径工具 ===")

    try:
        # 先检查原始 PATH 环境变量
        raw_path = os.environ.get('PATH', '')
        logger.info(f"✅ 原始PATH长度: {len(raw_path)}")

        # 测试在PATH中查找文件
        # 分别测试每个功能，避免一个错误影响全部
        try:
            from anp_open_sdk.config import config
            python_paths = config.find_in_path("python3")
            if python_paths:
                logger.info(f"✅ 找到Python3: {python_paths[0]}")
            else:
                logger.warning("⚠️  未找到Python3")
        except Exception as e:
            logger.warning(f"⚠️  查找Python3时出错: {e}")


        # 测试路径信息
        path_info = config.get_path_info()
        logger.info(f"✅ 路径信息: {path_info}")

        # 测试添加路径到PATH（谨慎测试）
        test_path = "/tmp/test_path"
        if not os.path.exists(test_path):
            os.makedirs(test_path, exist_ok=True)

        original_path = os.environ.get('PATH', '')
        config.add_to_path(test_path)
        new_path = os.environ.get('PATH', '')

        logger.info(f"✅ 路径已添加: {test_path in new_path}")

        # 恢复原始PATH
        os.environ['PATH'] = original_path

        return True
    except Exception as e:
        logger.error(f"❌ 路径工具测试失败: {e}")
        return False



def test_config_persistence():
    """测试配置持久化"""
    logger.info("\n=== 测试8: 配置持久化 ===")

    try:
        from anp_open_sdk.config import config

        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_config_path = f.name
            f.write("""
anp_sdk:
  port: 9999
  host: "test-host"
llm:
  max_tokens: 256
""")

        # 使用临时配置创建新的配置实例
        from anp_open_sdk.config.unified_config import UnifiedConfig
        temp_config = UnifiedConfig(temp_config_path)

        logger.info(f"✅ 临时配置端口: {temp_config.anp_sdk.port}")
        logger.info(f"✅ 临时配置主机: {temp_config.anp_sdk.host}")

        # 修改并保存
        temp_config.anp_sdk.port = 7777
        success = temp_config.save()
        logger.info(f"✅ 配置保存成功: {success}")

        # 重新加载验证
        temp_config.reload()
        logger.info(f"✅ 重新加载后端口: {temp_config.anp_sdk.port}")

        # 清理
        os.unlink(temp_config_path)

        return True
    except Exception as e:
        logger.error(f"❌ 配置持久化测试失败: {e}")
        return False

def test_type_conversion():
    """测试类型转换"""
    logger.info("\n=== 测试9: 类型转换 ===")

    try:
        from anp_open_sdk.config import config

        # 设置不同类型的环境变量
        test_vars = {
            'TEST_BOOL_TRUE': 'true',
            'TEST_BOOL_FALSE': 'false',
            'TEST_INT': '12345',
            'TEST_FLOAT': '3.14159',
            'TEST_LIST': 'item1,item2,item3',
            'TEST_PATH': '/usr/local/bin',
        }

        for key, value in test_vars.items():
            os.environ[key] = value

        # 测试类型转换
        from anp_open_sdk.config.unified_config import UnifiedConfig

        # 创建临时配置测试类型转换
        temp_config_content = """
env_mapping:
  test_bool_true: TEST_BOOL_TRUE
  test_bool_false: TEST_BOOL_FALSE
  test_int: TEST_INT
  test_float: TEST_FLOAT
  test_list: TEST_LIST
  test_path: TEST_PATH

env_types:
  test_bool_true: boolean
  test_bool_false: boolean
  test_int: integer
  test_float: float
  test_list: list
  test_path: path
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(temp_config_content)
            temp_config_path = f.name

        temp_config = UnifiedConfig(temp_config_path)

        logger.info(f"✅ 布尔值(true): {temp_config.env.test_bool_true} ({type(temp_config.env.test_bool_true)})")
        logger.info(f"✅ 布尔值(false): {temp_config.env.test_bool_false} ({type(temp_config.env.test_bool_false)})")
        logger.info(f"✅ 整数: {temp_config.env.test_int} ({type(temp_config.env.test_int)})")
        logger.info(f"✅ 浮点数: {temp_config.env.test_float} ({type(temp_config.env.test_float)})")
        logger.info(f"✅ 列表: {temp_config.env.test_list} ({type(temp_config.env.test_list)})")
        logger.info(f"✅ 路径: {temp_config.env.test_path} ({type(temp_config.env.test_path)})")

        # 清理
        os.unlink(temp_config_path)

        return True
    except Exception as e:
        logger.error(f"❌ 类型转换测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    logger.info("\n=== 测试10: 错误处理 ===")

    try:
        from anp_open_sdk.config import config

        # 测试访问不存在的配置项
        try:
            nonexistent = config.nonexistent_section.nonexistent_item
            logger.error("❌ 应该抛出AttributeError")
            return False
        except AttributeError as e:
            logger.info(f"✅ 正确处理不存在的配置项: {e}")

        # 测试访问不存在的环境变量
        nonexistent_env = config.env.nonexistent_env_var
        logger.info(f"✅ 不存在的环境变量返回: {nonexistent_env}")

        # 测试访问不存在的敏感信息
        try:
            nonexistent_secret = config.secrets.nonexistent_secret
            logger.error("❌ 应该抛出AttributeError")
            return False
        except AttributeError as e:
            logger.info(f"✅ 正确处理不存在的敏感信息: {e}")

        return True
    except Exception as e:
        logger.error(f"❌ 错误处理测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    logger.info("🚀 开始统一配置系统测试")
    logger.info("=" * 50)

    tests = [
        test_basic_config_loading,
        test_attribute_access,
        test_environment_variables,
        test_path_resolution,
        test_secrets,
        test_path_tools,
        test_config_persistence,
        test_type_conversion,
        test_error_handling
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
                logger.info("✅ 通过")
            else:
                failed += 1
                logger.error("❌ 失败")
        except Exception as e:
            failed += 1
            logger.error(f"❌ 异常: {e}")

    logger.info("\n" + "=" * 50)
    logger.info(f"📊 测试结果: {passed} 通过, {failed} 失败")

    if failed == 0:
        logger.info("🎉 所有测试通过！统一配置系统工作正常。")
    else:
        logger.warning("⚠️  部分测试失败，请检查配置。")

    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)