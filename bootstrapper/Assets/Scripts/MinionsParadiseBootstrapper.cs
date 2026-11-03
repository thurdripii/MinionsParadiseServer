
using System;
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
        string healthUrl = ServerBaseUrl.TrimEnd('/') + "/health";

        using (WWW request = new WWW(healthUrl))
        {
            float startTime = Time.realtimeSinceStartup;

            while (!request.isDone)
            {
                if (Time.realtimeSinceStartup - startTime > RequestTimeoutSeconds)
                {
                    Debug.LogError("[MPB] Server timeout.");
                    yield break;
                }

                yield return null;
            }

            if (!string.IsNullOrEmpty(request.error))
            {
                Debug.LogError("[MPB] Connection failed: " + request.error);
                yield break;
            }

            Debug.Log("[MPB] Server response: " + request.text);
        }
    }
}
