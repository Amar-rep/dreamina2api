import _ from 'lodash';

export default {

    prefix: '/v1',

    get: {
        '/models': async () => {
            return {
                "data": [
                    {
                "id": "dreamina",
                "object": "model",
                "owned_by": "dreamina-free-api"
            },
            {
                "id": "dreamina-4.5",
                "object": "model",
                "owned_by": "dreamina-free-api",
                "description": "Dreamina AI Image Generation Model 4.5"
            },
            {
                "id": "dreamina-4.0",
                "object": "model",
                "owned_by": "dreamina-free-api",
                "description": "Dreamina AI Image Generation Model 4.0"
            },
            {
                "id": "dreamina-video-3.0",
                        "object": "model",
                        "owned_by": "dreamina-free-api",
                        "description": "Dreamina AI Video Generation Model 3.0"
                    },
                    {
                        "id": "dreamina-video-3.0-pro",
                        "object": "model",
                        "owned_by": "dreamina-free-api",
                        "description": "Dreamina AI Video Generation Model 3.0 Pro"
                    },
                    {
                        "id": "dreamina-video-2.0",
                        "object": "model",
                        "owned_by": "dreamina-free-api",
                        "description": "Dreamina AI Video Generation Model 2.0"
                    },
                    {
                        "id": "dreamina-video-2.0-pro",
                        "object": "model",
                        "owned_by": "dreamina-free-api",
                        "description": "Dreamina AI Video Generation Model 2.0 Pro"
                    }
                ]
            };
        }

    }
}
