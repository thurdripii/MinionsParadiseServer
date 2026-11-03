
using System.Collections;
using UnityEngine;

public class MinionsParadiseBootstrapper : MonoBehaviour
{
    [Header("Server Settings")]
    public string ServerBaseUrl = "http://127.0.0.1:8000";
    public float RequestTimeoutSeconds = 15f;

    private void Start()
    {
        StartCoroutine(CheckServer());
    }

    private IEnumerator CheckServer()
    {
        string baseUrl = ServerBaseUrl.TrimEnd('/');

        yield return StartCoroutine(RequestEndpoint(baseUrl + "/health"));
        yield return StartCoroutine(RequestEndpoint(baseUrl + "/config"));
    }

    private IEnumerator RequestEndpoint(string url)
    {
        using (WWW request = new WWW(url))
        {
            float startTime = Time.realtimeSinceStartup;

            while (!request.isDone)
            {
                if (Time.realtimeSinceStartup - startTime > RequestTimeoutSeconds)
                {
                    Debug.LogError("[MPB] Timeout: " + url);
                    yield break;
                }

                yield return null;
            }

            if (!string.IsNullOrEmpty(request.error))
            {
                Debug.LogError("[MPB] Request failed: " + request.error);
                yield break;
            }

            Debug.Log("[MPB] Response from " + url);
            Debug.Log(request.text);
        }
    }
}
