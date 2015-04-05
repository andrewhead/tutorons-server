package com.headstrong;

import java.io.IOException;
import java.io.OutputStream;
import java.util.Map;
import java.util.HashMap;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;


public class NlgServer {

    /* Code snippet from http://stackoverflow.com/questions/11640025/java-httpserver-httpexchange-get */
    public static Map<String, String> queryToMap(String query){
        Map<String, String> result = new HashMap<String, String>();
        for (String param : query.split("&")) {
            String pair[] = param.split("=");
            if (pair.length > 1) {
                result.put(pair[0], pair[1]);
            } else{
                result.put(pair[0], "");
            }
        }
        return result;
    }

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/test", new MyHandler());
        server.setExecutor(null);
        server.start();

        /*
        JSONObject obj = new JSONObject();
        obj.put("subject", "Johnny");
        System.out.println(obj.toString());

        JSONParser parser = new JSONParser();
        String sentence = "";
        try {
            JSONObject parsedObj = (JSONObject) parser.parse(
                "{" +
                "\"verb\": \"be\"" +
                "\"subject\": \"the light\"" + 
                "\"object\": \"on\"" +
                "\"tense\": \"PAST\"" +
                "}"
            );
            sentence = toString(parsedObj);
        } catch (ParseException pe) {
            pe.printStackTrace();
        }
        System.out.println(sentence);
        */
    }

    static class MyHandler implements HttpHandler {
        public void handle(HttpExchange t) throws IOException {
            Map<String, String> params = queryToMap(t.getRequestURI().getQuery());
            JSONParser parser = new JSONParser();
            try {
                String specStr = params.get("spec").replace("+", " ");;
                System.out.println(specStr);
                JSONObject spec = (JSONObject) parser.parse(specStr);
                String response = packageResponse(generateSentence(spec)).toString();
                t.sendResponseHeaders(200, response.length());
                OutputStream os = t.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } catch (ParseException pe) {
                pe.printStackTrace();
            }
        }
    }

    public static JSONObject packageResponse(String msg) {
        JSONObject obj = new JSONObject();
        obj.put("msg", msg);
        return obj;
    }

    public static String generateSentence(JSONObject spec) {
        Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);
        SPhraseSpec p = nlgFactory.createClause();
        p.setSubject(spec.get("subject"));
        p.setVerb(spec.get("verb"));
        p.setObject(spec.get("object"));
        p.setFeature(Feature.TENSE, Tense.valueOf((String) spec.get("tense")));
        return realiser.realiseSentence(p);
    }

}
