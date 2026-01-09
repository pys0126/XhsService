from service.logic import XhsLogic


xhs_logic: XhsLogic = XhsLogic()

# 获取用户笔记列表
# response = xhs_logic.get_user_notes(user_id="60ae2ccd000000000101c7bd", xsec_token="ABWmyxguRSEPAC9GK04l453BxNIXXt4eqJfc9W1mc1fc4=")
# print(response.get("notes", []))

# 获取笔记详情
# response = xhs_logic.get_note_by_id(note_id="6809bac8000000000b01ee79", xsec_token="AB7lrCWslhUrZJqf-QuwYLVPL_B26kNuPVyoooytH9UDI=")

# 获取评论列表
# response = xhs_logic.get_comment_list(note_id="6954bbec0000000022033432", xsec_token="ABUN_1XSqLnjriCqCbVauqogsQ7WUawkzwAIqmfpI8Jfo=")
# print(response.get("comments", []))

# 获取子评论列表
# response = xhs_logic.get_sub_comment_list(note_id="6954bbec0000000022033432", comment_id="695e8990000000001702d553",
#                                           xsec_token="ABUN_1XSqLnjriCqCbVauqogsQ7WUawkzwAIqmfpI8Jfo=",
#                                           cursor="695ee1330000000016024111")
# print(response.get("comments", []))
