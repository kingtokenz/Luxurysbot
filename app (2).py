response_text = KNOWLEDGE_BASE["branches"]
            elif any(word in text for word in ["order", "buy", "how to"]):
                response_text = KNOWLEDGE_BASE["order"]
            elif any(word in text for word in ["return", "refund", "issue"]):
                response_text = KNOWLEDGE_BASE["return"]
            elif any(word in text for word in ["quality", "different", "best"]):
                response_text = KNOWLEDGE_BASE["quality"]

            send_whatsapp_message(recipient_id, response_text)
    except Exception as e:
        print(f"Error processing message: {e}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
