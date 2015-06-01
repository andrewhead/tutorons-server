import py4j.GatewayServer;

/**
 * Server to enable Python access to CSS explainer.
 */
public class CssExplainerEntryPoint {

    private CssExplainer explainer;

    public CssExplainerEntryPoint() {
        explainer = new CssExplainer();
    }

    public CssExplainer getExplainer() {
        return explainer;
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new CssExplainerEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}