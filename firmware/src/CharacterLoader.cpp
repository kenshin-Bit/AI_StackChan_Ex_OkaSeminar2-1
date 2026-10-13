#include "CharacterLoader.h"
#include <SD.h>
#include <SPIFFS.h>

// 設定の置き場所。SDカードを使わない構成では本体内蔵メモリから読む。
#if defined(ARDUINO_M5STACK_ATOMS3R) || defined(CONFIG_FROM_SPIFFS)
  #define CHARACTER_FS SPIFFS
#else
  #define CHARACTER_FS SD
#endif
#include <ArduinoJson.h>
#include <ArduinoYaml.h>

bool loadCharacter(const String& name, CharacterData& data) {
    if (name.isEmpty()) return false;

    String path = String("/characters/") + name + ".yaml";
    File file = CHARACTER_FS.open(path.c_str());
    if (!file) {
        Serial.printf("[Character] File not found: %s\n", path.c_str());
        return false;
    }

    // ファイルを一度すべて読み込み、空でないことを確かめてから解析する。
    // 【重要】存在しないキャラ名を指定すると、本体内蔵メモリ(SPIFFS)では open() が
    // 失敗せず「中身0バイトのファイル」が返ることがある。それを YAML ライブラリに渡すと
    // 解析結果が空のまま進み、ライブラリ内部で空ポインタを読んで本体が再起動を繰り返す
    // （実機で確認。SC_ExConfig.yaml の character.name が存在しない butler を指していた）。
    String content = file.readString();
    file.close();
    Serial.printf("[Character] Read %s (%u bytes)\n", path.c_str(), (unsigned)content.length());
    if (content.length() == 0) {
        // 空のまま解析に進むとライブラリが落ちるので、ここで止める
        Serial.println("[Character] File is empty. Skip.");
        return false;
    }

    DynamicJsonDocument doc(4096);
    auto err = deserializeYml(doc, content.c_str());

    if (err) {
        Serial.printf("[Character] YAML parse error: %s\n", err.c_str());
        return false;
    }

    if (!doc["system_prompt"].is<const char*>()) {
        Serial.println("[Character] system_prompt not found");
        return false;
    }

    data.systemPrompt        = doc["system_prompt"].as<String>();
    data.talkPrompt  = doc["talk_prompt"].as<String>();
    data.selfTalkPrompt      = doc["self_talk_prompt"].as<String>();
    data.voice               = doc["voice"].as<String>();
    data.memory              = doc["memory"] | false;

    Serial.printf("[Character] Loaded: %s (voice=%s memory=%s)\n",
                  name.c_str(),
                  data.voice.isEmpty() ? "default" : data.voice.c_str(),
                  data.memory ? "true" : "false");
    return true;
}
