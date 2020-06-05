# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestHTML::test_initial_form 1'] = '''
<!-- uncomment to use django.contrib.comments -->

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Submit Review</title>
    <meta name="description" content="Review Description">
    <meta name="author" content="Kelvin Jayanoris">
    <style>
        .grid {
            display: flex;
            flex-wrap: wrap;
        }

        .column {
            box-sizing: border-box;
            flex: 1;
        }

        .bigger {
            flex: 2.5;
        }

        .halves .column {
            flex: 0 0 50%;
        }

        .thirds .column {
            flex: 0 0 33.3333%;
        }

        .fourths .column {
            flex: 0 0 25%;
        }

        @media (max-width: 900px) {
            .grid {
                display: block;
            }
        }
    </style>
    <style>
        section {
            display: flex;
            flex-flow: row wrap;
        }

        section>div {
            flex: 1;
            padding: 0.5rem;
        }

        input[type="radio"] {
            display: none;
        }

        input[type="radio"]:not(:disabled)~label {
            cursor: pointer;
        }

        input[type="radio"]:disabled~label {
            color: #bcc2bf;
            border-color: #bcc2bf;
            box-shadow: none;
            cursor: not-allowed;
        }

        label {
            display: block;
            background: white;
            border-radius: 3%;
            padding: 0.7rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #5562eb;
        }

        .btnbtn {
            display: block;
            width: 100%;
            background: #4CAF50;
            color: white;
            border-radius: 3%;
            padding: 1rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #4CAF50;
            cursor: pointer;
            font-weight: 900;
        }

        .btnbtn.info {
            cursor: not-allowed;
        }

        .btnbtn.rejected {
            background: #ff0000;
        }

        hr {
            margin: 1rem 0;
        }

        .review_reason {
            background-color: aliceblue;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border-radius: 5%;
        }

        .review_reason::after {
            content: "";
            position: absolute;
            top: -1.2rem;
            left: 2rem;
            border: 1rem solid transparent;
            border-bottom-color: aliceblue;
            display: block;
            width: 0;
        }

        .comment-item {
            background-color: #fbfbff;
            margin-bottom: 0.6rem;
        }

        .comment-header {
            margin-top: 0.2rem;
            margin-bottom: -0.5rem;
            font-size: 0.9rem;
            color: #828282;
        }

        .commentarea textarea {
            margin-top: 1rem;
        }

        .commentarea button {
            margin-top: 0.5rem;
        }

        .btn-comment {
            display: block;
            padding: 0.2rem;
            text-align: center;
            cursor: pointer;
        }

        textarea {
            width: 100%;
        }

        input[type="radio"]:checked+label {
            background: #5562eb;
            color: white;
        }

        input[type="radio"]#review-reject:checked+label {
            background: #ff0000;
            border-color: #ff0000;
        }

        @media only screen and (max-width: 700px) {
            section {
                flex-direction: column;
            }
        }

        .content-box {
            margin: 0 auto;
            max-width: 800px;
        }

        .non-field-errors,
        .hidden-field-errors,
        .status-field-errors {
            font-size: 0.9rem;
            color: #ff0000;
        }

        .status-field-errors div {
            padding: 0 0.5rem;
        }
    </style>
</head>

<body>
    <div class="content-box">
        <h1 style="text-align: center;">Submit Review</h1>
        <div class="grid">
            <div class="column">
                <p>Please submit a review for this item</p>
                <!--
                    This section is meant to output details on the item being
                    reviewed so that a review can make an informed decision.
                -->
            </div>
            <div class="column">
                <form method="POST" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="CSRF-I_LOVE-OOV">

                    

                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="review" value="12408" id="id_review">
                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="reviewer" id="id_reviewer">
                    

                    
                        <section id="id_review_status">
                            <div>
                                <input type="radio" id="review-approve" name="review_status" value="1">
                                <label for="review-approve">Approve</label>
                            </div>
                            <div>
                                <input type="radio" id="review-reject" name="review_status" value="2">
                                <label for="review-reject">Reject</label>
                            </div>
                        </section>
                        
                        <section>
                            <div>
                                <button type="submit" class="btnbtn">Submit Review</button>
                            </div>
                        </section>
                    
                </form>
            </div>
        </div>
        
        <div class="grid" style="position:relative;">
            <div class="column review_reason">
                <p>Taking some time off after the current Reveal contract(s) come to an end.</p>
            </div>
        </div>
        
        <!-- COMMENTS SECTION -->
        <!-- uncomment these to show comments list and form using django.contrib.comments -->
        <!-- <hr /> -->
        
        
        <!-- End of comments -->
        <!-- END COMMENTS SECTION -->
    </div>
</body>

</html>
'''

snapshots['TestHTML::test_form_errors 1'] = '''
<!-- uncomment to use django.contrib.comments -->

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Submit Review</title>
    <meta name="description" content="Review Description">
    <meta name="author" content="Kelvin Jayanoris">
    <style>
        .grid {
            display: flex;
            flex-wrap: wrap;
        }

        .column {
            box-sizing: border-box;
            flex: 1;
        }

        .bigger {
            flex: 2.5;
        }

        .halves .column {
            flex: 0 0 50%;
        }

        .thirds .column {
            flex: 0 0 33.3333%;
        }

        .fourths .column {
            flex: 0 0 25%;
        }

        @media (max-width: 900px) {
            .grid {
                display: block;
            }
        }
    </style>
    <style>
        section {
            display: flex;
            flex-flow: row wrap;
        }

        section>div {
            flex: 1;
            padding: 0.5rem;
        }

        input[type="radio"] {
            display: none;
        }

        input[type="radio"]:not(:disabled)~label {
            cursor: pointer;
        }

        input[type="radio"]:disabled~label {
            color: #bcc2bf;
            border-color: #bcc2bf;
            box-shadow: none;
            cursor: not-allowed;
        }

        label {
            display: block;
            background: white;
            border-radius: 3%;
            padding: 0.7rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #5562eb;
        }

        .btnbtn {
            display: block;
            width: 100%;
            background: #4CAF50;
            color: white;
            border-radius: 3%;
            padding: 1rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #4CAF50;
            cursor: pointer;
            font-weight: 900;
        }

        .btnbtn.info {
            cursor: not-allowed;
        }

        .btnbtn.rejected {
            background: #ff0000;
        }

        hr {
            margin: 1rem 0;
        }

        .review_reason {
            background-color: aliceblue;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border-radius: 5%;
        }

        .review_reason::after {
            content: "";
            position: absolute;
            top: -1.2rem;
            left: 2rem;
            border: 1rem solid transparent;
            border-bottom-color: aliceblue;
            display: block;
            width: 0;
        }

        .comment-item {
            background-color: #fbfbff;
            margin-bottom: 0.6rem;
        }

        .comment-header {
            margin-top: 0.2rem;
            margin-bottom: -0.5rem;
            font-size: 0.9rem;
            color: #828282;
        }

        .commentarea textarea {
            margin-top: 1rem;
        }

        .commentarea button {
            margin-top: 0.5rem;
        }

        .btn-comment {
            display: block;
            padding: 0.2rem;
            text-align: center;
            cursor: pointer;
        }

        textarea {
            width: 100%;
        }

        input[type="radio"]:checked+label {
            background: #5562eb;
            color: white;
        }

        input[type="radio"]#review-reject:checked+label {
            background: #ff0000;
            border-color: #ff0000;
        }

        @media only screen and (max-width: 700px) {
            section {
                flex-direction: column;
            }
        }

        .content-box {
            margin: 0 auto;
            max-width: 800px;
        }

        .non-field-errors,
        .hidden-field-errors,
        .status-field-errors {
            font-size: 0.9rem;
            color: #ff0000;
        }

        .status-field-errors div {
            padding: 0 0.5rem;
        }
    </style>
</head>

<body>
    <div class="content-box">
        <h1 style="text-align: center;">Submit Review</h1>
        <div class="grid">
            <div class="column">
                <p>Please submit a review for this item</p>
                <!--
                    This section is meant to output details on the item being
                    reviewed so that a review can make an informed decision.
                -->
            </div>
            <div class="column">
                <form method="POST" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="CSRF-I_LOVE-OOV">

                    

                    
                        <ul class="hidden-field-errors">
                            
                                
                                    <li>Please ensure that you are reviewing the correct item.</li>
                                
                            
                        </ul>
                        <input type="hidden" name="review" value="1337" id="id_review">
                    
                        <ul class="hidden-field-errors">
                            
                                
                                    <li>Please ensure that you are reviewing the correct item.</li>
                                
                            
                        </ul>
                        <input type="hidden" name="reviewer" value="1337" id="id_reviewer">
                    

                    
                        <section id="id_review_status">
                            <div>
                                <input type="radio" id="review-approve" name="review_status" value="1">
                                <label for="review-approve">Approve</label>
                            </div>
                            <div>
                                <input type="radio" id="review-reject" name="review_status" value="2">
                                <label for="review-reject">Reject</label>
                            </div>
                        </section>
                        
                            <section class="status-field-errors"><div>Please submit an approval or rejection.</div></section>
                        
                        <section>
                            <div>
                                <button type="submit" class="btnbtn">Submit Review</button>
                            </div>
                        </section>
                    
                </form>
            </div>
        </div>
        
        <!-- COMMENTS SECTION -->
        <!-- uncomment these to show comments list and form using django.contrib.comments -->
        <!-- <hr /> -->
        
        
        <!-- End of comments -->
        <!-- END COMMENTS SECTION -->
    </div>
</body>

</html>
'''

snapshots['TestHTML::test_review_approved 1'] = '''
<!-- uncomment to use django.contrib.comments -->

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Submit Review</title>
    <meta name="description" content="Review Description">
    <meta name="author" content="Kelvin Jayanoris">
    <style>
        .grid {
            display: flex;
            flex-wrap: wrap;
        }

        .column {
            box-sizing: border-box;
            flex: 1;
        }

        .bigger {
            flex: 2.5;
        }

        .halves .column {
            flex: 0 0 50%;
        }

        .thirds .column {
            flex: 0 0 33.3333%;
        }

        .fourths .column {
            flex: 0 0 25%;
        }

        @media (max-width: 900px) {
            .grid {
                display: block;
            }
        }
    </style>
    <style>
        section {
            display: flex;
            flex-flow: row wrap;
        }

        section>div {
            flex: 1;
            padding: 0.5rem;
        }

        input[type="radio"] {
            display: none;
        }

        input[type="radio"]:not(:disabled)~label {
            cursor: pointer;
        }

        input[type="radio"]:disabled~label {
            color: #bcc2bf;
            border-color: #bcc2bf;
            box-shadow: none;
            cursor: not-allowed;
        }

        label {
            display: block;
            background: white;
            border-radius: 3%;
            padding: 0.7rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #5562eb;
        }

        .btnbtn {
            display: block;
            width: 100%;
            background: #4CAF50;
            color: white;
            border-radius: 3%;
            padding: 1rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #4CAF50;
            cursor: pointer;
            font-weight: 900;
        }

        .btnbtn.info {
            cursor: not-allowed;
        }

        .btnbtn.rejected {
            background: #ff0000;
        }

        hr {
            margin: 1rem 0;
        }

        .review_reason {
            background-color: aliceblue;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border-radius: 5%;
        }

        .review_reason::after {
            content: "";
            position: absolute;
            top: -1.2rem;
            left: 2rem;
            border: 1rem solid transparent;
            border-bottom-color: aliceblue;
            display: block;
            width: 0;
        }

        .comment-item {
            background-color: #fbfbff;
            margin-bottom: 0.6rem;
        }

        .comment-header {
            margin-top: 0.2rem;
            margin-bottom: -0.5rem;
            font-size: 0.9rem;
            color: #828282;
        }

        .commentarea textarea {
            margin-top: 1rem;
        }

        .commentarea button {
            margin-top: 0.5rem;
        }

        .btn-comment {
            display: block;
            padding: 0.2rem;
            text-align: center;
            cursor: pointer;
        }

        textarea {
            width: 100%;
        }

        input[type="radio"]:checked+label {
            background: #5562eb;
            color: white;
        }

        input[type="radio"]#review-reject:checked+label {
            background: #ff0000;
            border-color: #ff0000;
        }

        @media only screen and (max-width: 700px) {
            section {
                flex-direction: column;
            }
        }

        .content-box {
            margin: 0 auto;
            max-width: 800px;
        }

        .non-field-errors,
        .hidden-field-errors,
        .status-field-errors {
            font-size: 0.9rem;
            color: #ff0000;
        }

        .status-field-errors div {
            padding: 0 0.5rem;
        }
    </style>
</head>

<body>
    <div class="content-box">
        <h1 style="text-align: center;">Submit Review</h1>
        <div class="grid">
            <div class="column">
                <p>Please submit a review for this item</p>
                <!--
                    This section is meant to output details on the item being
                    reviewed so that a review can make an informed decision.
                -->
            </div>
            <div class="column">
                <form method="POST" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="CSRF-I_LOVE-OOV">

                    

                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="review" value="12410" id="id_review">
                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="reviewer" id="id_reviewer">
                    

                    
                        <section>
                            <div>
                                <button type="button" class="btnbtn info" disabled>Approved</button>
                            </div>
                        </section>
                    
                </form>
            </div>
        </div>
        
        <!-- COMMENTS SECTION -->
        <!-- uncomment these to show comments list and form using django.contrib.comments -->
        <!-- <hr /> -->
        
        
        <!-- End of comments -->
        <!-- END COMMENTS SECTION -->
    </div>
</body>

</html>
'''

snapshots['TestHTML::test_review_rejected 1'] = '''
<!-- uncomment to use django.contrib.comments -->

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Submit Review</title>
    <meta name="description" content="Review Description">
    <meta name="author" content="Kelvin Jayanoris">
    <style>
        .grid {
            display: flex;
            flex-wrap: wrap;
        }

        .column {
            box-sizing: border-box;
            flex: 1;
        }

        .bigger {
            flex: 2.5;
        }

        .halves .column {
            flex: 0 0 50%;
        }

        .thirds .column {
            flex: 0 0 33.3333%;
        }

        .fourths .column {
            flex: 0 0 25%;
        }

        @media (max-width: 900px) {
            .grid {
                display: block;
            }
        }
    </style>
    <style>
        section {
            display: flex;
            flex-flow: row wrap;
        }

        section>div {
            flex: 1;
            padding: 0.5rem;
        }

        input[type="radio"] {
            display: none;
        }

        input[type="radio"]:not(:disabled)~label {
            cursor: pointer;
        }

        input[type="radio"]:disabled~label {
            color: #bcc2bf;
            border-color: #bcc2bf;
            box-shadow: none;
            cursor: not-allowed;
        }

        label {
            display: block;
            background: white;
            border-radius: 3%;
            padding: 0.7rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #5562eb;
        }

        .btnbtn {
            display: block;
            width: 100%;
            background: #4CAF50;
            color: white;
            border-radius: 3%;
            padding: 1rem;
            margin-bottom: 0;
            text-align: center;
            position: relative;
            border: 1px solid #4CAF50;
            cursor: pointer;
            font-weight: 900;
        }

        .btnbtn.info {
            cursor: not-allowed;
        }

        .btnbtn.rejected {
            background: #ff0000;
        }

        hr {
            margin: 1rem 0;
        }

        .review_reason {
            background-color: aliceblue;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border-radius: 5%;
        }

        .review_reason::after {
            content: "";
            position: absolute;
            top: -1.2rem;
            left: 2rem;
            border: 1rem solid transparent;
            border-bottom-color: aliceblue;
            display: block;
            width: 0;
        }

        .comment-item {
            background-color: #fbfbff;
            margin-bottom: 0.6rem;
        }

        .comment-header {
            margin-top: 0.2rem;
            margin-bottom: -0.5rem;
            font-size: 0.9rem;
            color: #828282;
        }

        .commentarea textarea {
            margin-top: 1rem;
        }

        .commentarea button {
            margin-top: 0.5rem;
        }

        .btn-comment {
            display: block;
            padding: 0.2rem;
            text-align: center;
            cursor: pointer;
        }

        textarea {
            width: 100%;
        }

        input[type="radio"]:checked+label {
            background: #5562eb;
            color: white;
        }

        input[type="radio"]#review-reject:checked+label {
            background: #ff0000;
            border-color: #ff0000;
        }

        @media only screen and (max-width: 700px) {
            section {
                flex-direction: column;
            }
        }

        .content-box {
            margin: 0 auto;
            max-width: 800px;
        }

        .non-field-errors,
        .hidden-field-errors,
        .status-field-errors {
            font-size: 0.9rem;
            color: #ff0000;
        }

        .status-field-errors div {
            padding: 0 0.5rem;
        }
    </style>
</head>

<body>
    <div class="content-box">
        <h1 style="text-align: center;">Submit Review</h1>
        <div class="grid">
            <div class="column">
                <p>Please submit a review for this item</p>
                <!--
                    This section is meant to output details on the item being
                    reviewed so that a review can make an informed decision.
                -->
            </div>
            <div class="column">
                <form method="POST" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="CSRF-I_LOVE-OOV">

                    

                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="review" value="12411" id="id_review">
                    
                        <ul class="hidden-field-errors">
                            
                        </ul>
                        <input type="hidden" name="reviewer" id="id_reviewer">
                    

                    
                        <section>
                            <div>
                                <button type="button" class="btnbtn info rejected" disabled>Rejected</button>
                            </div>
                        </section>
                    
                </form>
            </div>
        </div>
        
        <!-- COMMENTS SECTION -->
        <!-- uncomment these to show comments list and form using django.contrib.comments -->
        <!-- <hr /> -->
        
        
        <!-- End of comments -->
        <!-- END COMMENTS SECTION -->
    </div>
</body>

</html>
'''
